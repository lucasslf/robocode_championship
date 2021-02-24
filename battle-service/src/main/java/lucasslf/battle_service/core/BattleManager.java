package lucasslf.battle_service.core;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lucasslf.battle_service.domain.Battle;
import lucasslf.battle_service.domain.Robot;
import lucasslf.battle_service.domain.RobotRepository;

import lucasslf.battle_service.event.BattleFinishedEvent;
import lucasslf.battle_service.infra.KafkaSender;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;
import java.util.stream.Collectors;

@Component
public class BattleManager {

    @Autowired
    RobotRepository robotRepository;

    @Autowired
    KafkaSender messageSender;


    public void runBattle(Battle battle){
        System.out.println("Preparing battle "+battle);
        List<Robot> robots = robotRepository.findAll();

        Map<UUID, String> robotMap = robots.stream().collect(Collectors.toMap(robot -> robot.getId(), robot -> robot.getFileName().substring(0, robot.getFileName().indexOf('_'))));
        try {
            Runtime rt = Runtime.getRuntime();
            String[] commands = {"java", "-cp", "robocode_libs/*", "StandAloneRobocodeBattleRunner", battle.getId().toString(), robotMap.get(battle.getRobot1()), robotMap.get(battle.getRobot2()) };
            System.out.println("Command: "+ Arrays.stream(commands).reduce("", (command, element) -> command+" "+element));
            System.out.println("Starting");
            Process battleProcess = rt.exec(commands);
            Thread newThread = new Thread(() -> {
                BufferedReader stdInput = new BufferedReader(new
                        InputStreamReader(battleProcess.getInputStream()));

                BufferedReader stdError = new BufferedReader(new
                        InputStreamReader(battleProcess.getErrorStream()));

                // Read the output from the command
                System.out.println("Robocode battle output:\n");
                String s = null;
                Map<String, BattleResult> battleResults = new HashMap<String, BattleResult>();
                try{
                    while ((s = stdInput.readLine()) != null) {
                        if(s.contains("BattleResult")){
                            System.out.println("RESULT");
                            ObjectMapper mapper = new ObjectMapper();
                            Map<String, BattleResult> mapResult = mapper.readValue(s, new TypeReference<Map<String, BattleResult>>() {});
                            battleResults.put(mapResult.get("BattleResult").getRobotName(), mapResult.get("BattleResult"));
                        }
                    }
                    String robot1Name = robotMap.entrySet().stream().filter(e -> e.getKey().equals(battle.getRobot1())).findFirst().get().getValue();
                    String robot2Name = robotMap.entrySet().stream().filter(e -> e.getKey().equals(battle.getRobot2())).findFirst().get().getValue();
                    if(battleResults.size() == 2) {

                        BattleFinishedEvent event = new BattleFinishedEvent(battle.getChampionshipId(), battle.getRobot1(), battle.getRobot2(), battleResults.get(robot1Name), battleResults.get(robot2Name) );
                        messageSender.sendBattleFinishedEvent(event);
                    }else{
                        System.out.println("BATTLE "+battle+" "+robot1Name+" vs "+robot2Name+ " FAILED!");
                    }
                    // Read any errors from the attempted command
                    System.out.println("Errors:\n");
                    while ((s = stdError.readLine()) != null) {
                        System.out.println(s);
                    }
                }catch (IOException ex){
                    ex.printStackTrace();
                }
            });
            newThread.start();
        }catch (IOException ex){
            ex.printStackTrace();
        }

    }


}



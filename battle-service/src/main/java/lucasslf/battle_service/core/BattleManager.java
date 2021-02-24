package lucasslf.battle_service.core;

import lucasslf.battle_service.domain.Battle;
import lucasslf.battle_service.domain.Robot;
import lucasslf.battle_service.domain.RobotRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Component
public class BattleManager {

    @Autowired
    RobotRepository robotRepository;

    public void runBattle(Battle battle){
        System.out.println("Preparing battle "+battle);
        List<Robot> robots = robotRepository.findAll();

        Map<UUID, String> robotMap = robots.stream().collect(Collectors.toMap(robot -> robot.getId(), robot -> robot.getFileName().substring(0, robot.getFileName().lastIndexOf('_'))));
        try {
            Runtime rt = Runtime.getRuntime();
            String[] commands = {"java", "-cp", "robocode_libs/*", "StandAloneRobocodeBattleRunner", battle.getId().toString(), robotMap.get(battle.getRobot1()), robotMap.get(battle.getRobot2()) };
            System.out.println("Command: "+ Arrays.stream(commands).reduce("", (command, element) -> command+" "+element));
            System.out.println("Starting");
            Process proc = rt.exec(commands);
            BufferedReader stdInput = new BufferedReader(new
                    InputStreamReader(proc.getInputStream()));

            BufferedReader stdError = new BufferedReader(new
                    InputStreamReader(proc.getErrorStream()));

            // Read the output from the command
            System.out.println("Here is the standard output of the command:\n");
            String s = null;
            while ((s = stdInput.readLine()) != null) {
                System.out.println(s);
            }

            // Read any errors from the attempted command
            System.out.println("Here is the standard error of the command (if any):\n");
            while ((s = stdError.readLine()) != null) {
                System.out.println(s);
            }
        }catch (IOException ex){
            ex.printStackTrace();
        }

//        BattleRunner battleRunner = new BattleRunner(battle, robotMap);
//
//        battleRunner.doRunBattle();

    }

}



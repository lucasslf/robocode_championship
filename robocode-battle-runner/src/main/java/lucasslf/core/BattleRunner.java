package lucasslf.core;


import net.sf.robocode.io.Logger;
import robocode.control.*;
import robocode.control.events.BattleAdaptor;
import robocode.control.events.BattleCompletedEvent;
import robocode.control.events.BattleErrorEvent;

import java.io.File;
import java.util.UUID;

public class BattleRunner{

    private final String robot1;
    private final String robot2;
    private final UUID battleId;
    private final String robocodeHome;

    public BattleRunner(UUID battleId, String robot1, String robot2) {
        this.battleId = battleId;
        this.robot1 = robot1;
        this.robot2 = robot2;
        this.robocodeHome = System.getProperty("lucasslf.robocode.home", "./");
    }

    public void doRunBattle(){
        System.out.println("robocode home: "+this.robocodeHome);
        RobocodeEngine engine = new RobocodeEngine(new File(this.robocodeHome));
        try {

            engine.addBattleListener(new BattleObserver());

            // Setup the battle specification

            int numberOfRounds = 50;
            BattlefieldSpecification battlefield = new BattlefieldSpecification(800, 600); // 800x600
            String selectedRobotNames = robot1+","+robot2;

            System.out.println(">>>" + selectedRobotNames);

            RobotSpecification[] selectedRobots = engine.getLocalRepository(selectedRobotNames);

            BattleSpecification battleSpec = new BattleSpecification(numberOfRounds, battlefield, selectedRobots);

            engine.runBattle(battleSpec, true);
        }catch (Exception ex){
            System.out.println(">>>>>>>>ERROR");
            ex.printStackTrace();
        }finally {
            engine.close();
        }

    }

    class BattleObserver extends BattleAdaptor {
        @Override
        public void onBattleError(final BattleErrorEvent event) {
            Logger.realErr.println(event.getError());
        }

        @Override
        public void onBattleCompleted(final BattleCompletedEvent event) {
            RobotResults[] lastResults = RobotResults.convertResults(event.getSortedResults());
            for(RobotResults a : lastResults){
                BattleResult r = new BattleResult(
                        battleId,
                        a.getRobot().getName(),
                        a.getScore(),
                        a.getSurvival(),
                        a.getLastSurvivorBonus(),
                        a.getBulletDamage(),
                        a.getRamDamage(),
                        a.getRamDamageBonus(),
                        a.getFirsts(),
                        a.getSeconds()
                );
                System.out.println(r);
            }
        }
    }

}

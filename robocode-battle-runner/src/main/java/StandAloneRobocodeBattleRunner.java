import lucasslf.core.BattleRunner;

import java.util.UUID;


public class StandAloneRobocodeBattleRunner {

    public static void main(String[] args) {
        if(args.length != 3){
            System.out.println("Wrong number of args");
            System.exit(-1);
        }

        UUID battleId = UUID.fromString(args[0]);
        BattleRunner battleRunner = new BattleRunner(battleId, args[1],  args[2]);
        battleRunner.doRunBattle();
    }
}

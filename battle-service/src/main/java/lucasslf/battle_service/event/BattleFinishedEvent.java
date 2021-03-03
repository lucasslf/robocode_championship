package lucasslf.battle_service.event;

import lucasslf.battle_service.core.BattleResult;


import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.temporal.Temporal;
import java.util.UUID;

public class BattleFinishedEvent {

    private final UUID id;
    private final UUID championshipId;
    private final UUID battleId;
    private final UUID robot1;
    private final UUID robot2;
    private final BattleResult robot1BattleResult;
    private final BattleResult robot2BattleResult;
    private final String event = "BattleFinished";
    private final Temporal createdAt;

    public BattleFinishedEvent(UUID championshipId, UUID robot1, UUID robot2, BattleResult robot1BattleResult, BattleResult robot2BattleResult) {
        this.id = UUID.randomUUID();
        this.championshipId = championshipId;
        this.battleId = UUID.fromString(robot1BattleResult.getBattleId());
        this.robot1 = robot1;
        this.robot2 = robot2;
        this.robot1BattleResult = robot1BattleResult;
        this.robot2BattleResult = robot2BattleResult;
        this.createdAt = LocalDateTime.now();
    }

    public String toString() {

        return "{"
                + "\"id\":\"" + id + "\""
                + ", \"championship_id\":\"" + championshipId + "\""
                + ", \"battle_id\":\"" + battleId + "\""
                + ", \"robot_1\":\"" + robot1 + "\""
                + ", \"robot_2\":\"" + robot2 + "\""
                + ", \"battle_result_robot_1\":" + robot1BattleResult
                + ", \"battle_result_robot_2\":" + robot2BattleResult
                + ", \"event\":\"" + event + "\""
                + ", \"created_at\":\"" + DateTimeFormatter.ISO_DATE_TIME.format(createdAt) + "\""
                + "}";
    }

}

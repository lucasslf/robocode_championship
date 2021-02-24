package lucasslf.battle_service.event;

import java.util.UUID;

public class BattleCreatedEvent {

    private final UUID id;
    private final UUID battleId;
    private final UUID championshipId;
    private final UUID robot1;
    private final UUID robot2;
    private final String event = "BattleCreated";

    public BattleCreatedEvent(UUID id, UUID battleId, UUID championshipId, UUID robot1, UUID robot2) {
        this.id = id;
        this.battleId = battleId;
        this.championshipId = championshipId;
        this.robot1 = robot1;
        this.robot2 = robot2;
    }


    public UUID getId() {
        return id;
    }

    public UUID getBattleId() {
        return battleId;
    }

    public UUID getChampionshipId() {
        return championshipId;
    }

    public UUID getRobot1() {
        return robot1;
    }

    public UUID getRobot2() {
        return robot2;
    }

    public String getEvent() {
        return event;
    }

}

package lucasslf.battle_service.domain;

import java.util.UUID;

public class Battle {
    private final UUID id;
    private final UUID championshipId;
    private final UUID robot1;
    private final UUID robot2;

    public Battle(UUID id, UUID championshipId, UUID robot1, UUID robot2) {
        this.id = id;
        this.championshipId = championshipId;
        this.robot1 = robot1;
        this.robot2 = robot2;
    }

    @Override
    public String toString() {
        return "Battle{" +
                "id=" + id +
                ", championshipId=" + championshipId +
                ", robot1=" + robot1 +
                ", robot2=" + robot2 +
                '}';
    }

    public UUID getId() {
        return id;
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
}

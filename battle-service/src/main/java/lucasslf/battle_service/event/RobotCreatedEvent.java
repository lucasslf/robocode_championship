package lucasslf.battle_service.event;

import java.util.UUID;

public class RobotCreatedEvent {
    private final UUID id;
    private final UUID robotId;
    private final String robotName;
    private final String robotURL;
    private final String event = "RobotCreated";

    public RobotCreatedEvent(UUID id, UUID robotId, String robotName, String robotURL) {
        this.id = id;
        this.robotId = robotId;
        this.robotName = robotName;
        this.robotURL = robotURL;
    }

    public UUID getId() {
        return id;
    }

    public UUID getRobotId() {
        return robotId;
    }

    public String getRobotName() {
        return robotName;
    }

    public String getRobotURL() {
        return robotURL;
    }

    public String getEvent() {
        return event;
    }
}

package lucasslf.battle_service.infra;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lucasslf.battle_service.event.BattleCreatedEvent;
import lucasslf.battle_service.event.RobotCreatedEvent;
import lucasslf.battle_service.service.BattleService;
import lucasslf.battle_service.service.RobotService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.UUID;


@Component
public class KafkaConsumer {

    static String BATTLE_CREATED_EVENT = "BattleCreated";
    static String ROBOT_CREATED_EVENT = "RobotCreated";

    @Autowired
    RobotService robotService;

    @Autowired
    BattleService battleService;



    @KafkaListener(topics = "robot-championship.championships", groupId = "battle-service")
    public void listenToChampionshipEvents(@Payload String event) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> map = mapper.readValue(event, new TypeReference<Map<String, Object>>() {
        });
        if (BATTLE_CREATED_EVENT.equals(map.get("event"))) {
            BattleCreatedEvent battleCreatedEvent = new BattleCreatedEvent(
                    UUID.fromString((String)map.get("id")),
                    UUID.fromString((String)map.get("battle_id")),
                    UUID.fromString((String)map.get("championship_id")),
                    UUID.fromString((String)map.get("robot_1")),
                    UUID.fromString((String)map.get("robot_2"))
            );
            battleService.handle(battleCreatedEvent);
        }
    }

    @KafkaListener(topics = "robot-championship.robots", groupId = "battle-service")
    public void listenToRobotsEvents(@Payload String event) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        Map<String, String> map = mapper.readValue(event, new TypeReference<Map<String, String>>() {
        });
        if (ROBOT_CREATED_EVENT.equals(map.get("event"))) {
            RobotCreatedEvent robotCreatedEvent = new RobotCreatedEvent(
                    UUID.fromString(map.get("id")),
                    UUID.fromString(map.get("robot_id")),
                    map.get("robot_name"),
                    map.get("robot_url")
            );
            robotService.handle(robotCreatedEvent);
        }
    }
}

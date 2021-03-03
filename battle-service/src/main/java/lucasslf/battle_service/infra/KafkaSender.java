package lucasslf.battle_service.infra;

import lucasslf.battle_service.event.BattleFinishedEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class KafkaSender {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    public void sendBattleFinishedEvent(BattleFinishedEvent event) {
        System.out.println("Sending Battle Finished event: "+event.toString());
        kafkaTemplate.send("robot-championship.championships", event.toString());
    }
}
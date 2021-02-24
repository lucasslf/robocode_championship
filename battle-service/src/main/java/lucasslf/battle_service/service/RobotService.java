package lucasslf.battle_service.service;

import lucasslf.battle_service.domain.Robot;
import lucasslf.battle_service.domain.RobotRepository;
import lucasslf.battle_service.event.RobotCreatedEvent;
import lucasslf.battle_service.infra.RobotDownloader;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.net.MalformedURLException;
import java.net.URL;

@Component
public class RobotService {

    @Autowired
    RobotRepository repository;

    public void handle(RobotCreatedEvent event){
        Robot robot = new Robot(event.getRobotId(), event.getRobotName(), event.getRobotURL());
        repository.insert(robot);
        RobotDownloader.downloadRobot(robot);
    }
}

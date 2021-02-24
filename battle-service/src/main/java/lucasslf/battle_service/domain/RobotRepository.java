package lucasslf.battle_service.domain;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.UUID;

public interface RobotRepository extends MongoRepository<Robot, UUID> {
}

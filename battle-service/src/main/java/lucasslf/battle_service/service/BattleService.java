package lucasslf.battle_service.service;

import lucasslf.battle_service.core.BattleManager;
import lucasslf.battle_service.domain.Battle;
import lucasslf.battle_service.event.BattleCreatedEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class BattleService {

    @Autowired
    BattleManager battleManager;

    public void handle(BattleCreatedEvent event){
        Battle battle = new Battle(event.getBattleId(),event.getChampionshipId(), event.getRobot1(), event.getRobot2());
        battleManager.runBattle(battle);
    }
}

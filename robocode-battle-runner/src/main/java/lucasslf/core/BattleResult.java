package lucasslf.core;

import java.util.UUID;

public class BattleResult {

    private final UUID battleId;
    private final String robotName;
    private final int score;
    private final int survival;
    private final int survivalBonus;
    private final int bulletDamage;
    private final int ramDamageTimes2;
    private final int ramBonus;
    private final int firsts;
    private final int seconds;

    public BattleResult(UUID battleId, String robotName, int score, int survival, int survivalBonus, int bulletDamage, int ramDamageTimes2, int ramBonus, int firsts, int seconds) {
        this.battleId = battleId;
        this.robotName = robotName;
        this.score = score;
        this.survival = survival;
        this.survivalBonus = survivalBonus;
        this.bulletDamage = bulletDamage;
        this.ramDamageTimes2 = ramDamageTimes2;
        this.ramBonus = ramBonus;
        this.firsts = firsts;
        this.seconds = seconds;
    }

    @Override
    public String toString() {
        return "{\"BattleResult\":{"
                + "\"battleId\":\"" + battleId + "\""
                + ", \"robotName\":\"" + robotName + "\""
                + ", \"score\":\"" + score + "\""
                + ", \"survival\":\"" + survival + "\""
                + ", \"survivalBonus\":\"" + survivalBonus + "\""
                + ", \"bulletDamage\":\"" + bulletDamage + "\""
                + ", \"ramDamageTimes2\":\"" + ramDamageTimes2 + "\""
                + ", \"ramBonus\":\"" + ramBonus + "\""
                + ", \"firsts\":\"" + firsts + "\""
                + ", \"seconds\":\"" + seconds + "\""
                + "}}";
    }

    public UUID getBattleId() {
        return battleId;
    }

    public String getRobotName() {
        return robotName;
    }

    public int getScore() {
        return score;
    }

    public int getSurvival() {
        return survival;
    }

    public int getSurvivalBonus() {
        return survivalBonus;
    }

    public int getBulletDamage() {
        return bulletDamage;
    }

    public int getRamDamageTimes2() {
        return ramDamageTimes2;
    }

    public int getRamBonus() {
        return ramBonus;
    }

    public int getFirsts() {
        return firsts;
    }

    public int getSeconds() {
        return seconds;
    }
}

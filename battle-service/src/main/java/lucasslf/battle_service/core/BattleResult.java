package lucasslf.battle_service.core;


public class BattleResult {

    private  String battleId;
    private  String robotName;
    private  int score;
    private  int survival;
    private  int survivalBonus;
    private  int bulletDamage;
    private  int ramDamageTimes2;
    private  int ramBonus;
    private  int firsts;
    private  int seconds;

    public BattleResult(){

    }

    public BattleResult(String battleId, String robotName, int score, int survival, int survivalBonus, int bulletDamage, int ramDamageTimes2, int ramBonus, int firsts, int seconds) {
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
        return "{"
                + "\"battle_id\":\"" + battleId + "\""
                + ", \"robot_name\":\"" + robotName + "\""
                + ", \"score\":\"" + score + "\""
                + ", \"survival\":\"" + survival + "\""
                + ", \"survival_bonus\":\"" + survivalBonus + "\""
                + ", \"bullet_damage\":\"" + bulletDamage + "\""
                + ", \"ram_damage\":\"" + ramDamageTimes2 + "\""
                + ", \"ram_bonus\":\"" + ramBonus + "\""
                + ", \"firsts\":\"" + firsts + "\""
                + ", \"seconds\":\"" + seconds + "\""
                + "}";
    }

    public String getBattleId() {
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

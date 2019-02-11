package upv.dsic.BetaAgent;

import org.aiwolf.sample.lib.AbstractRoleAssignPlayer;

public class BetaRoleAssignPlayer extends AbstractRoleAssignPlayer {

	@Override
	public String getName() {
		return "BetaRoleAssignPlayer";
	}
	
	public BetaRoleAssignPlayer() {
		setSeerPlayer(new BetaSeer());
		setVillagerPlayer(new BetaVillager());
		setBodyguardPlayer(new BetaBodyguard());
		setMediumPlayer(new BetaMedium());
		setPossessedPlayer(new BetaPossessed());
		setWerewolfPlayer(new BetaWerewolf());
		
	}

}

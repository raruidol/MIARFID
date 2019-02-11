package upv.dsic.BetaAgent;

import org.aiwolf.client.lib.*;
import org.aiwolf.common.data.*;

/** 村人役エージェントクラス */
public class BetaVillager extends BetaBasePlayer {

	@Override
	protected void chooseVoteCandidate() {
		werewolves.clear();
		for (Judge j : divinationList) {
			// si existe una adivinacion que me acusa de lobo descubro al lobo
			if (j.getResult() == Species.WEREWOLF && (j.getTarget() == me)) {
				Agent candidate = j.getAgent();
				if (isAlive(candidate) && !werewolves.contains(candidate)) {
					werewolves.add(candidate);
				}
			}
		}
		// Comprueba incoherencias entre identificaciones
		for (Judge i : identList) {
			for (Judge k : identList) {
				if(i.getResult() != k.getResult() && i.getTarget() == k.getTarget()) {
					for (Judge j : divinationList) {
						if (j.getResult() == i.getResult() && j.getTarget() == i.getTarget()) {
							Agent candidate = k.getAgent();
							if (isAlive(candidate) && !werewolves.contains(candidate)) {
								werewolves.add(candidate);
							}
						}
						
						if (j.getResult() == k.getResult() && j.getTarget() == k.getTarget()) {
							Agent candidate = i.getAgent();
							if (isAlive(candidate) && !werewolves.contains(candidate)) {
								werewolves.add(candidate);
							}
						}
					}
					
				}
			}
		}
		
		//Comprueba incoherencias entre adivinaciones
		for (Judge i : divinationList) {
			for (Judge k : divinationList) {
				if(i.getResult() != k.getResult() && i.getTarget() == k.getTarget()) {
					for (Judge j : identList) {
						if (j.getResult() == i.getResult() && j.getTarget() == i.getTarget()) {
							Agent candidate = k.getAgent();
							if (isAlive(candidate) && !werewolves.contains(candidate)) {
								werewolves.add(candidate);
							}
						}
						
						if (j.getResult() == k.getResult() && j.getTarget() == k.getTarget()) {
							Agent candidate = i.getAgent();
							if (isAlive(candidate) && !werewolves.contains(candidate)) {
								werewolves.add(candidate);
							}
						}
					}
					
				}
			}
		}
			
			


		// si no he encontrado ningún hombre lobo escojo otro aleatorio 
		if (werewolves.isEmpty()) {
			if (!aliveOthers.contains(voteCandidate)) {
				voteCandidate = randomSelect(aliveOthers);
			}
		} else {
			if (!werewolves.contains(voteCandidate)) {
				voteCandidate = randomSelect(werewolves);
				// comunica la sospecha y vota
				if (canTalk) {
					talkQueue.offer(new Content(new EstimateContentBuilder(voteCandidate, Role.WEREWOLF)));
					talkQueue.offer(new Content(new RequestContentBuilder(null, new Content(new VoteContentBuilder(voteCandidate)))));
				}
			}
		}
	}
	
	public String talk() {
		// Revela falsa identidad para atraer a los lobos en la próxima votación
		if (!isCameout && !isCo(Role.SEER)) {
			talkQueue.offer(new Content(new ComingoutContentBuilder(me, Role.SEER)));
			isCameout = true;
		}
		return super.talk();
	}

	@Override
	public String whisper() {
		throw new UnsupportedOperationException();
	}

	@Override
	public Agent attack() {
		throw new UnsupportedOperationException();
	}

	@Override
	public Agent divine() {
		throw new UnsupportedOperationException();
	}

	@Override
	public Agent guard() {
		throw new UnsupportedOperationException();
	}

}

package upv.dsic.BetaAgent;

import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

import org.aiwolf.client.lib.*;
import org.aiwolf.common.data.*;
import org.aiwolf.common.net.*;

/**
 * 霊媒師役エージェントクラス
 */
public class BetaMedium extends BetaVillager {
	int comingoutDay;
	boolean isCameout;
	Deque<Judge> identQueue = new LinkedList<>();
	Map<Agent, Species> myIdentMap = new HashMap<>();

	@Override
	public void initialize(GameInfo gameInfo, GameSetting gameSetting) {
		super.initialize(gameInfo, gameSetting);
		comingoutDay = (int) (Math.random() * 3 + 1);
		isCameout = false;
		identQueue.clear();
		myIdentMap.clear();
	}

	@Override
	public void dayStart() {
		super.dayStart();
		// al iniciar el dia identifica al último muerto
		Judge ident = currentGameInfo.getMediumResult();
		if (ident != null) {
			identQueue.offer(ident);
			myIdentMap.put(ident.getTarget(), ident.getResult());
		}
	}

	@Override
	protected void chooseVoteCandidate() {
		werewolves.clear();
		// si revela identidad como medium detectar lobo
		for (Agent agent : aliveOthers) {
			if (comingoutMap.get(agent) == Role.MEDIUM) {
				werewolves.add(agent);
			}
		}
		// si adivinan que soy lobo o averiguo que algun muerto no se corresponde con adivinación -> es lobo
		for (Judge j : divinationList) {
			Agent agent = j.getAgent();
			Agent target = j.getTarget();
			if (j.getResult() == Species.WEREWOLF && (target == me || isKilled(target)) || (myIdentMap.containsKey(target) && j.getResult() != myIdentMap.get(target))) {
				if (isAlive(agent) && !werewolves.contains(agent)) {
					werewolves.add(agent);
				}
			}
		}
		// candidato random si no identifico ningun lobo
		if (werewolves.isEmpty()) {
			if (!aliveOthers.contains(voteCandidate)) {
				voteCandidate = randomSelect(aliveOthers);
			}
		} else {
			if (!werewolves.contains(voteCandidate)) {
				voteCandidate = randomSelect(werewolves);
				// comunica su deducción de lobo y lo vota
				if (canTalk) {
					talkQueue.offer(new Content(new EstimateContentBuilder(voteCandidate, Role.WEREWOLF)));
					talkQueue.offer(new Content(new RequestContentBuilder(null, new Content(new VoteContentBuilder(voteCandidate)))));
				}
			}
		}
	}

	@Override
	public String talk() {

		// si identifica un lobo muerto revela su identidad
		if (!isCameout && (!identQueue.isEmpty() && identQueue.peekLast().getResult() == Species.WEREWOLF)) {
			talkQueue.offer(new Content(new ComingoutContentBuilder(me, Role.MEDIUM)));
			isCameout = true;
		}
		// si he revelado mi rol publico las identificaciones
		if (isCameout) {
			while (!identQueue.isEmpty()) {
				Judge ident = identQueue.poll();
				talkQueue.offer(new Content(new IdentContentBuilder(ident.getTarget(), ident.getResult())));
			}
		}
		return super.talk();
	}

}

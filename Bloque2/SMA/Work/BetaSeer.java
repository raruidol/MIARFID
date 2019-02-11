package upv.dsic.BetaAgent;

import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.aiwolf.client.lib.*;
import org.aiwolf.common.data.*;
import org.aiwolf.common.net.*;

/**
 * 占い師役エージェントクラス
 */
public class BetaSeer extends BetaVillager {
	int comingoutDay;
	boolean isCameout;
	Deque<Judge> divinationQueue = new LinkedList<>();
	Map<Agent, Species> myDivinationMap = new HashMap<>();
	List<Agent> whiteList = new ArrayList<>();
	List<Agent> blackList = new ArrayList<>();
	List<Agent> grayList;
	List<Agent> semiWolves = new ArrayList<>();
	List<Agent> possessedList = new ArrayList<>();

	@Override
	public void initialize(GameInfo gameInfo, GameSetting gameSetting) {
		super.initialize(gameInfo, gameSetting);
		comingoutDay = (int) (Math.random() * 3 + 1);
		isCameout = false;
		divinationQueue.clear();
		myDivinationMap.clear();
		whiteList.clear();
		blackList.clear();
		grayList = new ArrayList<>();
		semiWolves.clear();
		possessedList.clear();
	}

	@Override
	public void dayStart() {
		super.dayStart();
		// 占い結果を待ち行列に入れる
		Judge divination = currentGameInfo.getDivineResult();
		if (divination != null) {
			divinationQueue.offer(divination);
			grayList.remove(divination.getTarget());
			if (divination.getResult() == Species.HUMAN) {
				whiteList.add(divination.getTarget());
			} else {
				blackList.add(divination.getTarget());
			}
			myDivinationMap.put(divination.getTarget(), divination.getResult());
		}
	}

	@Override
	protected void chooseVoteCandidate() {
		// comprueba cuantos lobos vivos quedan
		List<Agent> aliveWolves = new ArrayList<>();
		for (Agent a : blackList) {
			if (isAlive(a)) {
				aliveWolves.add(a);
			}
		}
		// si existe algun lobo vivo lo vota
		if (!aliveWolves.isEmpty()) {
			if (!aliveWolves.contains(voteCandidate)) {
				voteCandidate = randomSelect(aliveWolves);
				if (canTalk) {
					talkQueue.offer(new Content(new RequestContentBuilder(null, new Content(new VoteContentBuilder(voteCandidate)))));
				}
			}
			return;
		}
		// limpia la lista de lobos
		werewolves.clear();
		// si otro agente revela su identidad como seer es lobo NO! -> es sospechoso
		for (Agent a : aliveOthers) {
			if (comingoutMap.get(a) == Role.SEER) {
				grayList.add(a);
			}
		}
		// si identificación no encaja con mis adivinaciones añado lobo a la lista de lobos
		for (Judge j : identList) {
			Agent agent = j.getAgent();
			if ((myDivinationMap.containsKey(j.getTarget()) && j.getResult() != myDivinationMap.get(j.getTarget()))) {
				if (isAlive(agent) && !werewolves.contains(agent)) {
					werewolves.add(agent);
				}
			}
		}
		possessedList.clear();
		semiWolves.clear();
		for (Agent a : werewolves) {
			// si el agente lobo estaba en la lista de humanos -> es possessed
			if (whiteList.contains(a)) {
				if (!possessedList.contains(a)) {
					talkQueue.offer(new Content(new EstimateContentBuilder(a, Role.POSSESSED)));
					possessedList.add(a);
				}
			} else {
				semiWolves.add(a);
			}
		}
		if (!semiWolves.isEmpty()) {
			if (!semiWolves.contains(voteCandidate)) {
				voteCandidate = randomSelect(semiWolves);
				// si el agente lobo no esta en la lista de
				if (canTalk) {
					talkQueue.offer(new Content(new EstimateContentBuilder(voteCandidate, Role.WEREWOLF)));
				}
			}
		}
		// si hay algun sospechoso elige aleatoriamente entre estos
		else {
			if (!grayList.isEmpty()) {
				if (!grayList.contains(voteCandidate)) {
					voteCandidate = randomSelect(grayList);
				}
			}
			// si no tiene ningún registro escoge aleatoriamente entre los vivos
			else {
				if (!aliveOthers.contains(voteCandidate)) {
					voteCandidate = randomSelect(aliveOthers);
				}
			}
		}
	}

	@Override
	public String talk() {
		// si es el dia, ha adivinado un lobo se revela
		if (!isCameout && (!divinationQueue.isEmpty() && divinationQueue.peekLast().getResult() == Species.WEREWOLF)) {
			talkQueue.offer(new Content(new ComingoutContentBuilder(me, Role.SEER)));
			isCameout = true;
		}
		// si ya ha revelado el rol, dice los resultados de sus adivinaciones
		if (isCameout) {
			while (!divinationQueue.isEmpty()) {
				Judge ident = divinationQueue.poll();
				talkQueue.offer(new Content(new DivinedResultContentBuilder(ident.getTarget(), ident.getResult())));
			}
		}
		return super.talk();
	}

	@Override
	public Agent divine() {
		// escoge objetivo a adivinar de la lista
		if (!semiWolves.isEmpty()) {
			return randomSelect(semiWolves);
		}
		// si no escoge un candidato aleatorio entre los agentes no adivinados previamente que siguen vivos
		List<Agent> candidates = new ArrayList<>();
		for (Agent a : aliveOthers) {
			if (!myDivinationMap.containsKey(a)) {
				candidates.add(a);
			}
		}
		if (candidates.isEmpty()) {
			return null;
		}
		return randomSelect(candidates);
	}

}

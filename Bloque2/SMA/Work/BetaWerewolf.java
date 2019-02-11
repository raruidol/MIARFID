package upv.dsic.BetaAgent;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.aiwolf.client.lib.*;
import org.aiwolf.common.data.*;
import org.aiwolf.common.net.*;

/**
 * 人狼役エージェントクラス
 */
public class BetaWerewolf extends BetaBasePlayer {
	/** cuenta lobos */
	int numWolves;
	/** rol falso a actuar */
	Role fakeRole;
	/** dia de revelación del rol falso */
	int comingoutDay;
	/** num. turno revelar */
	int comingoutTurn;
	/** controla si se ha revelado */
	boolean isCameout;
	/** mapa con falsa información */
	Map<Agent, Species> fakeJudgeMap = new HashMap<>();
	/** cola con falsa informacion */
	Deque<Judge> fakeJudgeQueue = new LinkedList<>();
	/** lista de possessed */
	List<Agent> possessedList = new ArrayList<>();
	/** lista de lobos */
	List<Agent> werewolves;
	/** lista de humanos */
	List<Agent> humans;
	/** lista de villagers */
	List<Agent> villagers = new ArrayList<>();
	/** num. turno de hablar */
	int talkTurn;

	@Override
	public void initialize(GameInfo gameInfo, GameSetting gameSetting) {
		super.initialize(gameInfo, gameSetting);
		numWolves = gameSetting.getRoleNumMap().get(Role.WEREWOLF);
		werewolves = new ArrayList<>(gameInfo.getRoleMap().keySet());
		humans = new ArrayList<>();
		for (Agent a : aliveOthers) {
			if (!werewolves.contains(a)) {
				humans.add(a);
			}
		}
		// escoge aleatoriamente un rol
		List<Role> roles = new ArrayList<>();
		for (Role r : Arrays.asList(Role.VILLAGER, Role.SEER, Role.MEDIUM)) {
			if (gameInfo.getExistingRoles().contains(r)) {
				roles.add(r);
			}
		}
		fakeRole = randomSelect(roles);
		// de 1 a 3 dias aleatoriamente para revelar su rol
		comingoutDay = (int) (Math.random() * 3 + 1);
		// de 0 a 4 el turno para revelar su rol
		comingoutTurn = (int) (Math.random() * 5);
		isCameout = false;
		fakeJudgeMap.clear();
		fakeJudgeQueue.clear();
		possessedList.clear();
	}

	@Override
	public void update(GameInfo gameInfo) {
		super.update(gameInfo);
		// si existe incoherencia en la lista de adivinaciones es possessed
		for (Judge j : divinationList) {
			Agent agent = j.getAgent();
			if (!werewolves.contains(agent) && ((humans.contains(j.getTarget()) && j.getResult() == Species.WEREWOLF) || (werewolves.contains(j.getTarget()) && j.getResult() == Species.HUMAN))) {
				if (!possessedList.contains(agent)) {
					possessedList.add(agent);
					whisperQueue.offer(new Content(new EstimateContentBuilder(agent, Role.POSSESSED)));
				}
			}
		}
		villagers.clear();
		for (Agent agent : aliveOthers) {
			if (!werewolves.contains(agent) && !possessedList.contains(agent)) {
				villagers.add(agent);
			}
		}
	}

	private Judge getFakeJudge() {
		Agent target = null;
		// si el rol falso es seer añade a la lista de candidatos todos aquellos que no han revelado su rol
		if (fakeRole == Role.SEER) {
			List<Agent> candidates = new ArrayList<>();
			for (Agent a : aliveOthers) {
				if (!fakeJudgeMap.containsKey(a) && comingoutMap.get(a) != Role.SEER) {
					candidates.add(a);
				}
			}
			if (candidates.isEmpty()) {
				target = randomSelect(aliveOthers);
			} else {
				target = randomSelect(candidates);
			}
		}
		// si el rol falso es medium recupera la info del agente ejecutado
		else if (fakeRole == Role.MEDIUM) {
			target = currentGameInfo.getExecutedAgent();
		}
		if (target != null) {
			Species result = Species.HUMAN;
			// si el agente ejecutado se encuentra en la lista de humanos
			if (humans.contains(target)) {
				// cuenta el numero de lobos falsos
				int nFakeWolves = 0;
				for (Agent a : fakeJudgeMap.keySet()) {
					if (fakeJudgeMap.get(a) == Species.WEREWOLF) {
						nFakeWolves++;
					}
				}
				if (nFakeWolves < numWolves) {
					// si el número de lobos falsos es inferior al número de lobos reales, identifica a la victima como lobo
					if (possessedList.contains(target) || !isCo(target)) {
						if (Math.random() < 0.5) {
							result = Species.WEREWOLF;
						}
					}
					// si el número de lobos falsos es inferior al número de lobos reales, identifica a la victima como lobo
					else {
						result = Species.WEREWOLF;
					}
				}
			}
			return new Judge(day, me, target, result);
		}
		return null;
	}

	@Override
	public void dayStart() {
		super.dayStart();
		talkTurn = -1;
		if (day == 0) {
			whisperQueue.offer(new Content(new ComingoutContentBuilder(me, fakeRole)));
		}
		// añade a la cola y al mapa la entrada de juez falsificada
		else {
			Judge judge = getFakeJudge();
			if (judge != null) {
				fakeJudgeQueue.offer(judge);
				fakeJudgeMap.put(judge.getTarget(), judge.getResult());
			}
		}
	}

	/** 投票先候補を選ぶ */
	@Override
	protected void chooseVoteCandidate() {
		List<Agent> candidates = new ArrayList<>();
		// 占い師/霊媒師騙りの場合
		if (fakeRole != Role.VILLAGER) {
			// si identifica algun villager que se haya revelado con la identidad falsa del lobo o que en el juez falso sea lobo lo añade a candidatos
			for (Agent a : villagers) {
				if (comingoutMap.get(a) == fakeRole || fakeJudgeMap.get(a) == Species.WEREWOLF) {
					candidates.add(a);
				}
			}
			// añade cualquier candidato que en el juez falso no sea humano
			if (candidates.isEmpty()) {
				for (Agent a : villagers) {
					if (fakeJudgeMap.get(a) != Species.HUMAN) {
						candidates.add(a);
					}
				}
			}
		}
		// si no hay candidatos añade todos los villagers posibles
		if (candidates.isEmpty()) {
			candidates.addAll(villagers);
		}
		// si no hay candidatos añade los possessed
		if (candidates.isEmpty()) {
			candidates.addAll(possessedList);
		}
		if (!candidates.isEmpty()) {
			if (!candidates.contains(voteCandidate)) {
				voteCandidate = randomSelect(candidates);
				if (canTalk) {
					talkQueue.offer(new Content(new EstimateContentBuilder(voteCandidate, Role.WEREWOLF)));
				}
			}
		} else {
			voteCandidate = null;
		}
	}

	@Override
	public String talk() {
		talkTurn++;
		if (fakeRole != Role.VILLAGER) {
			if (!isCameout) {
				// comprueba el numero de seers y mediums falsos y "verdaderos" revelados
				int fakeSeerCo = 0;
				int fakeMediumCo = 0;
				int seerCo = 0;
				int mediumCo = 0;
				for (Agent b : villagers) {
					if (comingoutMap.get(b) == Role.SEER) {
						seerCo++;
					} else if (comingoutMap.get(b) == Role.MEDIUM) {
						mediumCo++;
					}
				}
				// si revelan roles de "verdadero" seer o medium pasa a actuar como villager
				if (fakeRole == Role.SEER && seerCo > 0 || fakeRole == Role.MEDIUM && mediumCo > 0) {
					fakeRole = Role.VILLAGER; 
					whisperQueue.offer(new Content(new ComingoutContentBuilder(me, fakeRole)));
				}
				
				for (Agent a : werewolves) {
					if (comingoutMap.get(a) == Role.SEER) {
						fakeSeerCo++;
					} else if (comingoutMap.get(a) == Role.MEDIUM) {
						fakeMediumCo++;
					}
				}
				// si revelan roles de falso seer o medium pasa a actuar como villager
				if (fakeRole == Role.SEER && fakeSeerCo > 0 || fakeRole == Role.MEDIUM && fakeMediumCo > 0) {
					fakeRole = Role.VILLAGER; 
					whisperQueue.offer(new Content(new ComingoutContentBuilder(me, fakeRole)));
				}
				/**
				else {
					// si algun agente ha revelado su rol como el rol falso del lobo se apresura en revelar su rol
					for (Agent a : humans) {
						if (comingoutMap.get(a) == fakeRole) {
							comingoutDay = day;
						}
					}
					// revela el rol falso a los demas agentes
					if (day >= comingoutDay && talkTurn >= comingoutTurn) {
						isCameout = true;
						talkQueue.offer(new Content(new ComingoutContentBuilder(me, fakeRole)));
					}
				}
				*/
			}
			// si esta roleando seer o medium lanza información falsa relativa a adivinaciones o identificaciones
			else {
				while (!fakeJudgeQueue.isEmpty()) {
					Judge judge = fakeJudgeQueue.poll();
					if (fakeRole == Role.SEER) {
						talkQueue.offer(new Content(new DivinedResultContentBuilder(judge.getTarget(), judge.getResult())));
					} else if (fakeRole == Role.MEDIUM) {
						talkQueue.offer(new Content(new IdentContentBuilder(judge.getTarget(), judge.getResult())));
					}
				}
			}
		}
		return super.talk();
	}

	/** 襲撃先候補を選ぶ */
	@Override
	protected void chooseAttackVoteCandidate() {
		// seer > medium > bodyguard > villager
		List<Agent> candidates = new ArrayList<>();
		for (Agent a : villagers) {
			if (isCo(a) && comingoutMap.get(a) == Role.SEER) {
				candidates.add(a);
			}
		}
		for (Agent b : villagers) {
			if (isCo(b) && comingoutMap.get(b) == Role.MEDIUM) {
				if(candidates.isEmpty()) {candidates.add(b);}
			}
		}
		for (Agent c : villagers) {
			if (isCo(c) && comingoutMap.get(c) == Role.BODYGUARD) {
				if(candidates.isEmpty()) {candidates.add(c);}
			}
		}
		// si no ha revelado nadie el rol añade todos los villagers
		if (candidates.isEmpty()) {
			candidates.addAll(villagers);
		}
		// si no quedan villagers los possessed
		if (candidates.isEmpty()) {
			candidates.addAll(possessedList);
		}
		if (!candidates.isEmpty()) {
			attackVoteCandidate = randomSelect(candidates);
		} else {
			attackVoteCandidate = null;
		}
	}

}

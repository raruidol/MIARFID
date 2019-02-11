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

/** clase basica sobre la que se construyen los roles */
public class BetaBasePlayer implements Player {
	/** agente propio */
	Agent me;
	/** nº del dia */
	int day;
	/** control talk */
	boolean canTalk;
	/** control whisper */
	boolean canWhisper;
	/** información actual de la partida */
	GameInfo currentGameInfo;
	/** lista de agentes vivos */
	List<Agent> aliveOthers;
	/** lista de agentes ejecutados */
	List<Agent> executedAgents = new ArrayList<>();
	/** lista de agentes asesinados */
	List<Agent> killedAgents = new ArrayList<>();
	/** lista de agentes adivinados seer */
	List<Judge> divinationList = new ArrayList<>();
	/** lista agentes medium */
	List<Judge> identList = new ArrayList<>();
	/** cola de talks */
	Deque<Content> talkQueue = new LinkedList<>();
	/** cola de whispers */
	Deque<Content> whisperQueue = new LinkedList<>();
	/** agente votado */
	Agent voteCandidate;
	/** agente declarado como voto */
	Agent declaredVoteCandidate;
	/** agente objetivo de ataque */
	Agent attackVoteCandidate;
	/** agente declarado como objetivo de ataque */
	Agent declaredAttackVoteCandidate;
	/** mapa de agentes revelados */
	Map<Agent, Role> comingoutMap = new HashMap<>();
	/** cabeza de la cola de talks */
	int talkListHead;
	/** lista de humanos */
	List<Agent> humans = new ArrayList<>();
	/** lista de lobos */
	List<Agent> werewolves = new ArrayList<>();
	/** controla si ha revelado el rol */
	boolean isCameout;

	/** comprueba si un agente sigue vivo */
	protected boolean isAlive(Agent agent) {
		return currentGameInfo.getStatusMap().get(agent) == Status.ALIVE;
	}

	/** comprueba si un agente ha sido ejecutado */
	protected boolean isKilled(Agent agent) {
		return killedAgents.contains(agent);
	}

	/** comprueba si un agente ha revelado su identidad */
	protected boolean isCo(Agent agent) {
		return comingoutMap.containsKey(agent);
	}

	/** comprueba si un agente ha revelado su rol */
	protected boolean isCo(Role role) {
		return comingoutMap.containsValue(role);
	}

	/** comprueba si un agente es humano */
	protected boolean isHuman(Agent agent) {
		return humans.contains(agent);
	}

	/** comprueba si un agente es hombre lobo */
	protected boolean isWerewolf(Agent agent) {
		return werewolves.contains(agent);
	}

	/** selecciona un item aleatorio en una lista */
	protected <T> T randomSelect(List<T> list) {
		if (list.isEmpty()) {
			return null;
		} else {
			return list.get((int) (Math.random() * list.size()));
		}
	}

	@Override
	public String getName() {
		return "MyBasePlayer";
	}

	@Override
	public void initialize(GameInfo gameInfo, GameSetting gameSetting) {
		day = -1;
		me = gameInfo.getAgent();
		aliveOthers = new ArrayList<>(gameInfo.getAliveAgentList());
		aliveOthers.remove(me);
		executedAgents.clear();
		killedAgents.clear();
		divinationList.clear();
		identList.clear();
		comingoutMap.clear();
		humans.clear();
		werewolves.clear();
		isCameout = false;
	}

	@Override
	public void update(GameInfo gameInfo) {
		currentGameInfo = gameInfo;
		// Actualiza la variable del numero del dia en caso de existir un cambio de dia en la partida
		if (currentGameInfo.getDay() == day + 1) {
			day = currentGameInfo.getDay();
			return;
		}
		
		// Registra los nuevos agentes ejecutados en la partida
		addExecutedAgent(currentGameInfo.getLatestExecutedAgent());
		// Gestión del proceso de talk durante el dia de la partida
		for (int i = talkListHead; i < currentGameInfo.getTalkList().size(); i++) {
			Talk talk = currentGameInfo.getTalkList().get(i);
			Agent talker = talk.getAgent();
			if (talker == me) {
				continue;
			}
			Content content = new Content(talk.getText());
			switch (content.getTopic()) {
			case COMINGOUT:
				comingoutMap.put(talker, content.getRole());
				break;
			case DIVINED:
				divinationList.add(new Judge(day, talker, content.getTarget(), content.getResult()));
				break;
			case IDENTIFIED:
				identList.add(new Judge(day, talker, content.getTarget(), content.getResult()));
				break;
			default:
				break;
			}
		}
		talkListHead = currentGameInfo.getTalkList().size();
	}

	@Override
	public void dayStart() {
		canTalk = true;
		canWhisper = false;
		if (currentGameInfo.getRole() == Role.WEREWOLF) {
			canWhisper = true;
		}
		talkQueue.clear();
		whisperQueue.clear();
		declaredVoteCandidate = null;
		voteCandidate = null;
		declaredAttackVoteCandidate = null;
		attackVoteCandidate = null;
		talkListHead = 0;
		// 前日に追放されたエージェントを登録
		addExecutedAgent(currentGameInfo.getExecutedAgent());
		// 昨夜死亡した（襲撃された）エージェントを登録
		if (!currentGameInfo.getLastDeadAgentList().isEmpty()) {
			addKilledAgent(currentGameInfo.getLastDeadAgentList().get(0));
		}
	}

	private void addExecutedAgent(Agent executedAgent) {
		if (executedAgent != null) {
			aliveOthers.remove(executedAgent);
			if (!executedAgents.contains(executedAgent)) {
				executedAgents.add(executedAgent);
			}
		}
	}

	private void addKilledAgent(Agent killedAgent) {
		if (killedAgent != null) {
			aliveOthers.remove(killedAgent);
			if (!killedAgents.contains(killedAgent)) {
				killedAgents.add(killedAgent);
			}
		}
	}

	/** 投票先候補を選びvoteCandidateにセットする */
	protected void chooseVoteCandidate() {
	}

	@Override
	public String talk() {
		chooseVoteCandidate();
		if (voteCandidate != null && voteCandidate != declaredVoteCandidate) {
			talkQueue.offer(new Content(new VoteContentBuilder(voteCandidate)));
			declaredVoteCandidate = voteCandidate;
		}
		return talkQueue.isEmpty() ? Talk.SKIP : talkQueue.poll().getText();
	}

	/** 襲撃先候補を選びattackVoteCandidateにセットする */
	protected void chooseAttackVoteCandidate() {
	}

	@Override
	public String whisper() {
		chooseAttackVoteCandidate();
		if (attackVoteCandidate != null && attackVoteCandidate != declaredAttackVoteCandidate) {
			whisperQueue.offer(new Content(new AttackContentBuilder(attackVoteCandidate)));
			declaredAttackVoteCandidate = attackVoteCandidate;
		}
		return whisperQueue.isEmpty() ? Talk.SKIP : whisperQueue.poll().getText();
	}

	@Override
	public Agent vote() {
		canTalk = false;
		chooseVoteCandidate();
		return voteCandidate;
	}

	@Override
	public Agent attack() {
		canWhisper = false;
		chooseAttackVoteCandidate();
		canWhisper = true;
		return attackVoteCandidate;
	}

	@Override
	public Agent divine() {
		return null;
	}

	@Override
	public Agent guard() {
		return null;
	}

	@Override
	public void finish() {
	}

}

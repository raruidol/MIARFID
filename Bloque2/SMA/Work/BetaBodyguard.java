package upv.dsic.BetaAgent;

import java.util.ArrayList;
import java.util.List;

import org.aiwolf.common.data.*;
import org.aiwolf.common.net.*;

/**
 * 狩人役エージェントクラス
 */
public class BetaBodyguard extends BetaVillager {
	/** agente protegido */
	Agent guardedAgent;

	@Override
	public void initialize(GameInfo gameInfo, GameSetting gameSetting) {
		super.initialize(gameInfo, gameSetting);
		guardedAgent = null;
	}

	@Override
	public Agent guard() {
		Agent guardCandidate = null;
		// 前日の護衛が成功しているようなら同じエージェントを護衛
		if (guardedAgent != null && isAlive(guardedAgent) && currentGameInfo.getLastDeadAgentList().isEmpty()) {
			guardCandidate = guardedAgent;
		}
		// 新しい護衛先の選定
		else {
			// en primer lugar escoge los agentes revelados como SEER
			List<Agent> candidates = new ArrayList<>();
			for (Agent agent : aliveOthers) {
				if (comingoutMap.get(agent) == Role.SEER && !werewolves.contains(agent)) {
					candidates.add(agent);
				}
			}
			// En segundo lugar opta por los Medium
			if (candidates.isEmpty()) {
				for (Agent agent : aliveOthers) {
					if (comingoutMap.get(agent) == Role.MEDIUM && !werewolves.contains(agent)) {
						candidates.add(agent);
					}
				}
			}
			// Si no existe ninguno de los anteriores escoge uno de los vivos que no sea lobo
			if (candidates.isEmpty()) {
				for (Agent agent : aliveOthers) {
					if (!werewolves.contains(agent)) {
						candidates.add(agent);
					}
				}
			}
			// caso trivial
			if (candidates.isEmpty()) {
				candidates.addAll(aliveOthers);
			}
			// escoge un agente aleatorio de los candidatos escogidos anteriormente
			guardCandidate = randomSelect(candidates);
		}
		guardedAgent = guardCandidate;
		return guardCandidate;
	}

}

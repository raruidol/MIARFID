import java.util.Random;
import java.util.Vector;

import negotiator.Bid;
import negoUPV.UPVAgent;

public class lastOfferSender extends UPVAgent {

	Bid last_moment_offer;
	double tresholdT = 0.95;
	double bestUtility = 0.0;
	double S;
	double beta;
	double RU;
	double utility;

	public void initialize() {
		last_moment_offer = null;
		beta = 5;
		RU = 0.8;
		S = 0.99;
		update();
	}

	public boolean acceptOffer(Bid offer) {
		utility = getUtility(offer);

		if (utility>bestUtility){
			bestUtility = utility;
			last_moment_offer = offer;
		}

		update();

		return utility >= S;
	}

	private void update() {

		S = 1 - (1 - RU)*Math.pow(getTime(),1.0/beta);

	}

	public Bid proposeOffer() {

		Bid selected;

		if (getTime()>tresholdT){
			selected = last_moment_offer;

		}
		else{
			Vector<Bid> m_bids = getOffers(S , S + 0.1);

			selected = m_bids.get(rand.nextInt(m_bids.size()));

		}
		return selected;

	}
}

import java.util.Random;
import java.util.Vector;

import negotiator.Bid;
import negoUPV.UPVAgent;

public class titForTat extends UPVAgent {

	Bid last_moment_offer;
	double lastUtSent = 0.0;
	double lastUtRec = 0.0;
	double last2UtRec = 0.0;
	double tresholdT = 0.95;
	int counter = 0;
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
		 utility=getUtility(offer);

		if(counter > 2){
			last2UtRec = lastUtRec;
			lastUtRec = getUtility(offer);
		}

		if (utility>bestUtility){
			bestUtility = utility;
			last_moment_offer = offer;
		}

		update();

		return utility >= S;
	}

	private void update() {

		if (counter > 3){

			S = Math.min(1.0, Math.max(RU, lastUtSent-(last2UtRec-lastUtRec)));
		}
		else{
			S = 1 - (1 - RU)*Math.pow(getTime(),1.0/beta);
		}
		counter+=1;

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

		lastUtSent = getUtility(selected);

		return selected;

	}
}

import java.util.Random;
import java.util.Vector;
import java.util.Collections;
import java.util.*;

import negotiator.Bid;
import negoUPV.UPVAgent;

public class caganer extends UPVAgent {

	Bid last_moment_offer;
	double lastUtSent = 0.0;
	double lastUtRec = 0.0;
	double last2UtRec = 0.0;
	double tresholdT = 0.999;
	int counter = 0;
	boolean flag = true;
	double bestUtility = 0.0;
	double p1utility = 0.0;
	double p2utility = 0.0;
	double S;
	double beta;
	double RU;
	double utility;

	public void initialize() {
		last_moment_offer = null;
		beta = 5;
		RU = 0.75;
		S = 0.99;
		update();
	}

	public boolean acceptOffer(Bid offer) {
		utility=getUtility(offer);

		if (flag){
 			p1utility = getUtility(offer);
 			p2utility = getUtility(offer);
			flag = false;
 		}

		if (counter%100 == 0){
			p1utility = p2utility;
			p2utility = getUtility(offer);
		}

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

		if(p1utility >= p2utility){
			if (counter > 3){
				S = Math.min(1.0, Math.max(RU, lastUtSent-(last2UtRec-lastUtRec)));
			}

			else{
				S = 1 - (1 - RU)*Math.pow(getTime(),1.0/beta);
			}
		}
		else{
			if(last2UtRec-lastUtRec < 0){
				S = Math.min(1.0, Math.max(RU, lastUtSent-(2*(last2UtRec-lastUtRec))));
			}
			else{
				S = Math.min(1.0, Math.max(RU, lastUtSent));
			}
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

			//selected = m_bids.get(rand.nextInt(m_bids.size()));


			Bid maxbid = m_bids.get(0);
			for (int i=1; i<m_bids.size(); i++){
				if ( getUtility(m_bids.get(i)) > getUtility(maxbid) && getUtility(m_bids.get(i)) != 1.0 ){
					maxbid = m_bids.get(i);
				}

			}

			selected = maxbid;
		}


		lastUtSent = getUtility(selected);

		return selected;

	}
}

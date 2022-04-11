using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Task : MonoBehaviour{
    public static Task task;

    public decimal slope, minhyp, maxhyp, target_p, initial_stim;
    public decimal[] false_alarm_rates = {0, 0.1m, 0.2m, 0.3m, 0.4m};
    public decimal[] p_yes;
    public int ntrials_a, n_catch_trials_a, ntrials_b, n_catch_trials_b, nhypotheses;

    // Start is called before the first frame update
    void Start(){
        if(task && task != this)
            Destroy(this);
        else
            task = this;
    }

    public void initTasks(decimal max){
        slope = 0.1m;

        minhyp = 100;
        maxhyp = max;

        nhypotheses = (int)max * 10;

        initial_stim = maxhyp;

        ntrials_a = 8;
        n_catch_trials_a = 3;
        ntrials_b = 6;
        n_catch_trials_b = 1;

        p_yes = new decimal[false_alarm_rates.Length];
        for(int i = 0; i < false_alarm_rates.Length; i++){
            p_yes[i] = (decimal)optimalp((float)false_alarm_rates[i]);
        }

        target_p = mean(p_yes);
    }

    public bool evaluate(decimal stim){
        //Get the participant's response for the given stimulus level. 
        return true;
    }

    public float optimalp(float a){
        return (2*a+1+Mathf.Sqrt(1+8*a))/(3+Mathf.Sqrt(1+8*a));
    }

    private decimal mean(decimal[] arr){
        decimal sum = 0;
        for(int i = 0; i < arr.Length; i++) {
            sum += arr[i];
        }
        return sum / arr.Length;
    }
}

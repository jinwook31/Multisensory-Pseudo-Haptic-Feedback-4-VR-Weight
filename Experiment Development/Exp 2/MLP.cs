using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class MLP : MonoBehaviour{
    public static MLP mlp;

    public static List<decimal[]> hypotheses = new List<decimal[]>();
    public List<string> trials;

    public decimal stim;
    private bool start = false;

    // Start is called before the first frame update
    void Start(){
        if(mlp && mlp != this)
            Destroy(this);
        else
            mlp = this;
    }

    public void startMLP(decimal maxhyp){
        trials = new List<string>();
        Task.task.initTasks(maxhyp);
        
        init_hypotheses(Task.task);
        stim = Task.task.initial_stim;
    }

    public float pyes(float x, float a, float m, float k){
        // Return the probability of a "yes" response,
        // given the logistic psychmetric function.
        // x is the stimulus intensity,
        // a is the false alarm rate
        // k is the slope parameter (fiddle with this so it gives the right transition range)
        // m is the mean of the distribution
        return a+((1-a)*(1/(1+Mathf.Exp(-k*(x-m)))));
    }

    public void init_hypotheses(Task task){
        List<string> trialsA = new List<string>();
        List<string> trialsB = new List<string>();

        generateTrials(trialsA, task.ntrials_a-1, "mlp");
        generateTrials(trialsA, task.n_catch_trials_a, "catch");
        generateTrials(trialsB, task.ntrials_b, "mlp");
        generateTrials(trialsB, task.n_catch_trials_b, "catch");
        ShuffleList(trialsA);
        ShuffleList(trialsB);

        trials.Add("mlp");
        trials.AddRange(trialsA);
        trials.AddRange(trialsB);

        decimal[] THRESHOLD_HYPOTHESES = LinSpace(task.minhyp, task.maxhyp, task.nhypotheses);

        for(int a = 0; a < task.false_alarm_rates.Length; a++){
            for(int m = 0; m < THRESHOLD_HYPOTHESES.Length; m++){
                decimal[] hypo = {task.false_alarm_rates[a], THRESHOLD_HYPOTHESES[m], 1};  //(a, m, p)
                hypotheses.Add(hypo);
            }
        }
    }

    public void updatehypotheses(decimal x, bool answer, Task task){
        List<decimal[]> newhyp = new List<decimal[]>();
        foreach(decimal[] hyp in hypotheses){
            decimal obsp = (decimal)pyes((float)x, (float)hyp[0], (float)hyp[1], (float)task.slope);
            if(!answer) obsp = 1 - obsp;
            decimal[] tmp = {hyp[0], hyp[1], hyp[2]*obsp};
            newhyp.Add(tmp);
        }
        hypotheses = newhyp;
    }

    public decimal[] getmaximumlikelihood(){
        float[] pArr = new float[hypotheses.Count];
        int index = 0;
        foreach(decimal[] hyp in hypotheses){
            pArr[index++] = (float)hyp[2];
        }
        float maxp = Mathf.Max(pArr);

        List<decimal[]> maxlikelihyps = new List<decimal[]>();
        foreach(decimal[] hyp in hypotheses){
            if((float)hyp[2] == maxp)
                maxlikelihyps.Add(hyp);
        }

        return maxlikelihyps[Random.Range(0, maxlikelihyps.Count)];
    }

    public float getsweetpoint(decimal[] target_p, decimal p, Task task){
        float a = (float)target_p[0], m = (float)target_p[1];
        if((float)p <= a){
            Debug.Log("Error, calculating a sweet point below the false alarm rate!");
            return 0;
        }
        float y = ((1-a)/((float)p-a))-1;
        return (Mathf.Log(y)/(-(float)task.slope)) + m;
    }


    private static void ShuffleList<T>(List<T> list){
        int random1;
        int random2;
 
        T tmp;
 
        for (int index = 0; index < list.Count; ++index){
            random1 = UnityEngine.Random.Range(0, list.Count);
            random2 = UnityEngine.Random.Range(0, list.Count);
 
            tmp = list[random1];
            list[random1] = list[random2];
            list[random2] = tmp;
        }
    }

    private void generateTrials(List<string> list, int mlp, string trial){
        for(int i=0; i <mlp; i++){
            list.Add(trial);
        }
    }

    private static decimal[] LinSpace(decimal start, decimal stop, int num, bool endpoint = true){
        decimal step = (stop - start) / (num - 1);
        decimal[] res = new decimal[num];
        for(int i = 0; i < num; i++){
            res[i] = start + step * i;
        }
        return res;
    }
}

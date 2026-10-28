# FORM 2
THE PATENTS ACT, 1970
(39 of 1970)
&
THE PATENTS RULES, 2003

## COMPLETE SPECIFICATION
(See section 10 and rule 13)

---

### 1. TITLE OF THE INVENTION
SYSTEM AND METHOD FOR PROSPECTIVE FAILURE WARNING IN AUTONOMOUS AGENTS USING TRAJECTORY RISK DECOMPOSITION

---

### 2. APPLICANT(S)
(a) NAME: [APPLICANT NAME / INSTITUTION]  
(b) NATIONALITY: [NATIONALITY, e.g., Indian]  
(c) ADDRESS: [OFFICIAL POSTAL ADDRESS WITH PIN CODE]  

---

### 3. PREAMBLE TO THE DESCRIPTION

#### COMPLETE SPECIFICATION
The following specification particularly describes the invention and the manner in which it is to be performed:

---

### 4. TECHNICAL FIELD OF THE INVENTION
The present invention relates to computer-implemented systems and methods for runtime monitoring of autonomous software agents during sequential task execution. Particularly, the present invention relates to prospective failure warning based on partially observed execution trajectories of autonomous agents. More particularly, the present invention relates to determining trajectory-associated failure risk, determining task-difficulty-associated failure risk, and decomposing the failure risk to identify a trajectory-dependent risk component for generating a prospective warning. The advantage of the present invention is to distinguish execution-dependent failure-risk information from failure risk attributable to task difficulty, thereby supporting earlier and more reliable warning decisions. The invention is suitable for autonomous agents that execute multi-step tasks through actions, observations, and interactions with software tools or computing environments.

---

### 5. BACKGROUND ART INCLUDING CITATIONS OF PRIOR ART
One of the prior art numbers, United States Patent No. US12441366B2, titled "Task-relevant failure detection for trajectory prediction in machines", describes a failure detection mechanism associated with trajectory prediction in which predicted trajectory information is evaluated to identify potentially problematic operating outcomes.

Another prior art no., United States Patent No. US12694133, titled "Autonomous agent observation and control", describes an observation and control architecture for autonomous software agents, including monitoring of agent states and execution of agent actions and providing mechanisms for agent control.

Yet another prior art no., United States Patent No. US12450494B1, titled "Validating autonomous artificial intelligence (AI) agents using generative AI", describes a validation framework for autonomous artificial intelligence agents in which executed actions are evaluated according to predefined risk or sensitivity considerations for monitoring and policy enforcement.

Another prior art no., arXiv preprint arXiv:2512.03109, titled "E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing", describes sequential monitoring of agent trajectories using intermediate verifier information and statistical decision procedures for making monitoring decisions while controlling false alarms.

Yet another prior art no., arXiv preprint arXiv:2608.03222, titled "Fail-Fast, Restart-Smart: Early Failure Prediction and Restart for SWE Agentic Tasks", describes early failure prediction for software engineering agents using information from partial execution trajectory prefixes to estimate the likelihood of eventual task failure and support early termination or restart decisions.

However, the cited prior art addresses trajectory prediction, agent observation and control, action-risk validation, sequential trajectory monitoring, or early failure prediction using respective monitoring or prediction signals. The cited prior art does not describe, in combination, a risk representation that distinguishes failure-risk information associated with an observed agent execution trajectory from failure-risk information associated with task or task-difficulty characteristics for prospective warning determination. Accordingly, there is a need for a computer-implemented approach for prospective monitoring of sequential autonomous-agent execution that can distinguish execution-associated failure-risk information from task-associated failure-risk information while processing information available during execution.

---

### 6. OBJECTS OF THE INVENTION
The principal object of this invention is to provide a computer-implemented method and system for prospective failure warning in autonomous agents during sequential task execution.

Another object of this invention is to provide a method for decomposing composite failure risk into a task-difficulty-associated failure risk component and a trajectory-associated failure risk component.

A further object of this invention is to provide a method for isolating a trajectory-dependent failure risk component from said composite failure risk for generating prospective failure warnings.

Yet another object of this invention is to provide a method for determining prospective failure warnings based on partially observed execution trajectories of autonomous agents.

Still another object of this invention is to provide a method for distinguishing execution-dependent failure-risk information from failure risk attributable to task difficulty during autonomous agent monitoring.

Further object of this invention is to provide a system and method applicable to autonomous agents that execute multi-step tasks through actions, observations, and interactions with software tools or computing environments.

---

### 7. SUMMARY OF THE INVENTION
The present invention addresses the technical problem of providing prospective failure warnings for autonomous agents during sequential task execution by distinguishing execution-dependent failure risk from task-difficulty-associated failure risk.

To achieve the objects, the present invention provides a solution comprising a computer-implemented method and system for decomposing composite failure risk into a task-difficulty-associated failure risk component and a trajectory-associated failure risk component, and generating prospective failure warnings based on the trajectory-associated failure risk component.

According to the basic aspect of the present invention, there is provided a method for prospective failure warning in autonomous agents, comprising receiving information from a partially observed execution trajectory of an autonomous agent, determining a task-difficulty-associated failure risk, determining a trajectory-associated failure risk, decomposing the failure risk to identify a trajectory-dependent risk component, and generating a prospective failure warning based on said trajectory-dependent risk component.

It is another aspect of the present invention to provide a system comprising one or more processors configured to execute the method for prospective failure warning, wherein the system receives execution telemetry from autonomous agents and outputs prospective failure warnings during agent execution.

It is one another aspect of the present invention to calibrate a decision threshold for the trajectory-dependent risk component using a calibration dataset to control false-alarm rates in the prospective failure warnings.

It is another aspect of the present invention that the method operates using only trajectory information available up to a partial execution point of the agent trajectory, without requiring information about the eventual outcome of the trajectory.

It is one another aspect of the present invention that the system and method are applicable to autonomous agents executing multi-step tasks through actions, observations, and interactions with software tools or computing environments. The advantages of the present invention include distinguishing execution-dependent failure-risk information from failure risk attributable to task difficulty and enabling prospective warning decisions to be generated from partially observed autonomous-agent execution trajectories while controlling false-alarm behavior.

---

### 8. BRIEF DESCRIPTION OF THE DRAWINGS
The embodiment of the present invention is illustrated with the help of accompanying drawings:

Fig. 1 illustrates a block diagram of a computer-implemented system for prospective failure warning in autonomous agents via trajectory risk decomposition, according to an embodiment of the present invention;

Fig. 2 illustrates a flowchart of a computer-implemented method for prospective failure warning from a partially observed agent trajectory, according to an embodiment of the present invention;

Fig. 3 illustrates a flowchart of a method for decision threshold calibration under a false-alarm rate constraint, according to an embodiment of the present invention; and

Fig. 4 illustrates a graphical representation of trajectory-dependent risk decomposition across execution prefixes, according to an embodiment of the present invention.

---

### 9. DETAILED DESCRIPTION OF THE INVENTION WITH REFERENCE TO THE ACCOMPANYING DRAWINGS
The invention is illustrated with the help of the accompanying drawings Fig. 1 to Fig. 4.

With reference to Fig. 1, the present invention provides a computer-implemented prospective failure warning system (100) configured to process partially observed execution trajectories of autonomous agents using trajectory risk decomposition.

The system (100) receives a partial trajectory input (102) corresponding to an autonomous agent executing a multi-step task up to an intermediate execution checkpoint t, where t represents an execution step within a predetermined processing horizon. The partial trajectory input (102) and associated task information are used to provide task characteristics input (104) and trajectory execution features input (108).

The task characteristics input (104) represents characteristics associated with the assigned task that are available independently of step-by-step execution dynamics, including task instructions, target environment specifications, prompt characteristics, and available tool definitions. The task characteristics input (104) is processed by a static task-difficulty model (106) configured to estimate a failure probability associated with task characteristics, thereby providing a static failure risk value P_static (112).

The trajectory execution features input (108) represents execution information observed up to checkpoint t, including information derived from sequential actions, tool interactions, execution events, system responses, errors, repetitions, resource usage, or execution timing. The trajectory execution features input (108) is processed by a dynamic trajectory risk model (110) configured to determine an execution-conditioned failure risk based on the partially observed trajectory, thereby providing a dynamic failure risk value P_dynamic(t) (114).

The static failure risk value P_static (112) and the dynamic failure risk value P_dynamic(t) (114) are supplied to a risk decomposition module (116). The risk decomposition module (116) computes a trajectory-dependent residual risk value R_t according to:

R_t = P_dynamic(t) - P_static

The residual risk value represents the difference between the execution-conditioned failure risk and the failure risk associated with task characteristics. The decomposition thereby provides a trajectory-dependent risk representation for prospective warning determination while distinguishing the task-difficulty-associated component from the execution-conditioned component.

The computed residual risk value R_t is supplied to a threshold comparison module (118). A calibrated decision threshold storage (120) provides a predetermined decision threshold tau*, which is calibrated using an independent calibration dataset under a predetermined false-alarm rate constraint. The threshold comparison module (118) determines whether the residual risk satisfies the warning condition:

R_t >= tau*

When the warning condition is satisfied, the threshold comparison module (118) generates a prospective failure warning through the prospective failure warning output (122).

According to one embodiment of the present invention, as shown in Fig. 2, a computer-implemented method for prospective failure warning is performed across successive partial execution checkpoints of an agent trajectory.

At step 200, the method receives a partial trajectory representing observed execution events of an autonomous agent up to checkpoint t.

At step 202, the method determines task characteristics and trajectory execution features available at the corresponding partial execution point without referencing the eventual terminal outcome of the trajectory.

At step 204, the task characteristics are processed to compute the static failure probability P_static.

At step 206, the trajectory execution features observed up to checkpoint t are processed to compute the dynamic failure probability P_dynamic(t). Steps 204 and 206 may be performed in parallel or in any order.

At step 208, the method computes the trajectory-dependent residual risk R_t by subtracting P_static from P_dynamic(t):

R_t = P_dynamic(t) - P_static

At step 210, a decision operation determines whether the computed residual risk satisfies the warning threshold criterion by evaluating R_t >= tau*, where tau* is the calibrated decision threshold retrieved from threshold storage (120).

If the residual risk meets or exceeds the threshold, the method proceeds to step 212, wherein a prospective failure warning is generated.

If the residual risk does not meet the threshold, the method proceeds to step 214, wherein no prospective failure warning is generated at the corresponding checkpoint and processing may continue to a subsequent execution checkpoint t+1.

According to another embodiment of the present invention, as shown in Fig. 3, the decision threshold tau* is determined through an offline calibration method constrained by a predetermined false-alarm rate.

At step 300, a calibration trajectory dataset comprising pre-recorded execution episodes of successful and failed tasks is ingested, wherein the calibration data are maintained separately from training and test data.

At step 302, static failure probabilities and dynamic failure probabilities are computed across partial execution prefixes in the calibration dataset.

At step 304, residual risk values R_calib are derived for the calibration prefixes by subtracting the respective static failure probability from the dynamic failure probability:

R_calib = P_dynamic - P_static

At step 306, the residual risk values are aggregated at episode level by determining a maximum residual risk for each episode according to:

R_max^(i) = max_t R_t^(i)

The resulting episode-level residual risk values are considered separately for successful and failed episodes.

At step 308, a plurality of candidate decision thresholds tau are evaluated across the resulting residual risk distributions.

At step 310, the false-alarm rate is determined for each candidate threshold using successful calibration episodes, wherein a successful episode contributes a false alarm when its episode-level maximum residual risk satisfies R_max >= tau.

At step 312, a decision threshold tau* is selected to maximize failure recall on the failed episodes in the calibration trajectory dataset subject to satisfying the predetermined false-alarm rate constraint.

At step 314, the selected decision threshold tau* is frozen and stored in threshold storage (120) for subsequent prospective warning generation and downstream evaluation.

According to yet another embodiment of the present invention, as shown in Fig. 4, the trajectory-dependent risk decomposition is graphically represented across execution prefixes up to a predetermined checkpoint horizon K.

The horizontal axis (402) represents the sequential execution prefix step t, and the vertical axis (404) represents the failure-risk and residual-risk scale.

In Panel A, the static task-difficulty failure risk representation (406) corresponds to the static failure risk P_static associated with the task characteristics. The dynamic trajectory failure risk curve (408) represents P_dynamic(t) determined from information available up to successive execution prefixes. The difference between the dynamic failure risk representation (408) and the static failure risk representation (406) represents the trajectory-dependent residual risk (410):

R_t = P_dynamic(t) - P_static

In Panel B, the trajectory-dependent residual risk (410) is represented with respect to the calibrated decision threshold (412), corresponding to tau*. A prospective warning trigger point (414) is reached when the residual risk satisfies the warning condition:

R_t >= tau*

Thus, the graphical representation distinguishes the decomposition of failure risk from the subsequent threshold comparison applied to the resulting trajectory-dependent residual risk.

---

### 10. CLAIMS

I/WE CLAIM:

1. A computer-implemented method for prospective failure warning in autonomous agents using trajectory risk decomposition, the method comprising:
   receiving a partial trajectory corresponding to an autonomous agent executing a multi-step task up to an intermediate execution checkpoint t within a predetermined processing horizon;
   obtaining a static failure risk value (P_static) representing failure risk associated with task characteristics of the multi-step task;
   determining a dynamic failure risk value (P_dynamic(t)) representing execution-conditioned failure risk determined from trajectory execution features observed up to the intermediate execution checkpoint t without referencing a terminal outcome of the multi-step task;
   computing, by a processor, a trajectory-dependent residual risk value (R_t) according to:
       R_t = P_dynamic(t) - P_static;
   retrieving a calibrated decision threshold (tau*) from a threshold storage, wherein the calibrated decision threshold is pre-calibrated on an independent calibration trajectory dataset under a predetermined false-alarm rate constraint;
   evaluating the trajectory-dependent residual risk value (R_t) against the calibrated decision threshold (tau*); and
   generating a prospective failure warning when the trajectory-dependent residual risk value satisfies:
       R_t >= tau*.

2. The method as claimed in claim 1, wherein the task characteristics are available independently of step-by-step execution dynamics of the autonomous agent and comprise one or more of: task instructions, target environment specifications, prompt characteristics, and available tool definitions.

3. The method as claimed in claim 1, wherein the trajectory execution features observed up to the intermediate execution checkpoint t comprise one or more of: sequential actions, tool interactions, execution events, system error responses, action repetitions, resource usage metrics, and execution step latency.

4. The method as claimed in claim 1, wherein when the trajectory-dependent residual risk value does not satisfy the condition R_t >= tau*, no prospective failure warning is generated at intermediate execution checkpoint t, and processing continues to a subsequent execution checkpoint t+1.

5. The method as claimed in claim 1, wherein the calibrated decision threshold (tau*) is obtained by:
   determining static failure probabilities and dynamic failure probabilities across a plurality of partial execution prefixes of pre-recorded episodes in the calibration trajectory dataset;
   deriving prefix-level residual risk values by subtracting the respective static failure probability from the dynamic failure probability;
   determining an episode-level maximum residual risk for each pre-recorded episode;
   evaluating candidate decision thresholds across the resulting episode-level maximum residual risks;
   determining a false-alarm rate for each candidate decision threshold across successful episodes in the calibration trajectory dataset;
   selecting the decision threshold (tau*) that maximizes failure recall on the failed episodes in the calibration trajectory dataset subject to satisfying the predetermined false-alarm rate constraint; and
   storing the selected decision threshold (tau*) in the threshold storage for subsequent warning determination.

6. The method as claimed in claim 1, wherein prospective failure warning determination is performed at intermediate execution checkpoints using information available up to the respective checkpoint and without referencing an eventual terminal outcome, the checkpoints being limited to a predetermined checkpoint horizon K.

7. A computer-implemented system (100) for prospective failure warning in autonomous agents using trajectory risk decomposition, the system comprising:
   one or more processors; and
   a memory communicatively coupled to the one or more processors, the memory storing instructions executable by the one or more processors to configure the system to:
       implement a static task-difficulty model (106) configured to determine a static failure risk value (P_static, 112) associated with task characteristics (104) of a multi-step task;
       implement a dynamic trajectory risk model (110) configured to determine a dynamic failure risk value (P_dynamic(t), 114) conditioned on trajectory execution features (108) observed from a partial trajectory input (102) up to an intermediate execution checkpoint t without referencing a terminal outcome;
       implement a risk decomposition module (116) configured to compute a trajectory-dependent residual risk value (R_t) according to:
           R_t = P_dynamic(t) - P_static;
       access a calibrated decision threshold storage (120) storing a decision threshold (tau*) calibrated under a predetermined false-alarm rate constraint; and
       implement a threshold comparison module (118) configured to evaluate the trajectory-dependent residual risk value (R_t) against the decision threshold (tau*) and generate a prospective failure warning output (122) when R_t >= tau*.

8. The system as claimed in claim 7, wherein the threshold comparison module (118) generates no prospective failure warning when R_t < tau* and enables processing of a subsequent intermediate execution checkpoint t+1.

---

### 11. ABSTRACT OF THE INVENTION

SYSTEM AND METHOD FOR PROSPECTIVE FAILURE WARNING IN AUTONOMOUS AGENTS USING TRAJECTORY RISK DECOMPOSITION

The present invention provides a computer-implemented system (100) and method for prospective failure warning during sequential task execution by autonomous agents. A partial trajectory input (102) provides task characteristics (104) and trajectory execution features (108). A static model (106) determines a task-difficulty failure risk P_static (112), while a dynamic model (110) determines an execution-conditioned failure risk P_dynamic(t) (114) up to checkpoint t without referencing terminal outcomes. A risk decomposition module (116) computes trajectory-dependent residual risk: R_t = P_dynamic(t) - P_static. A threshold comparison module (118) evaluates R_t against a calibrated decision threshold tau* in storage (120), calibrated under a predetermined false-alarm rate constraint. A prospective failure warning (122) is generated when R_t >= tau*. The technical advancement lies in distinguishing task-difficulty-associated failure risk from execution-conditioned failure risk for prospective warning determination. The invention applies to autonomous agents executing multi-step tasks in computing environments.

Accompanying Figure: Fig. 1

---

Dated this [Day] day of [Month], [Year]

[SIGNATURE]  
[NAME OF AGENT/APPLICANT]  
Patent Agent for the Applicant  
IN/PA No.: [AGENT REGISTRATION NUMBER]

import numpy as np
import scipy.stats as stats

N_SAMPLES = 100000

def p_rain(wind, cloudy):
    # P(rain = 1 | wind = wind, cloudy = cloudy)
    if wind == 1 and cloudy == 1: return 0.8
    if wind == 1 and cloudy == 0: return 0.4
    if wind == 0 and cloudy == 1: return 0.4
    if wind == 0 and cloudy == 0: return 0.1

def p_event(exams):
    # P(event = 1 | exams = exams)
    if exams == 1: return 0.02
    if exams == 0: return 0.7

def p_busy(rain, event, academic_holiday):
    # P(busy = 1 | rain = rain, event = event, academic_holiday = academic_holiday)
    if academic_holiday == 0:
        if rain == 1 and event == 1: return 0.01
        if rain == 1 and event == 0: return 0.2
        if rain == 0 and event == 1: return 0.65
        if rain == 0 and event == 0: return 0.7
    else:
        if rain == 1 and event == 1: return 0.01
        if rain == 1 and event == 0: return 0.015
        if rain == 0 and event == 1: return 0.4
        if rain == 0 and event == 0: return 0.55

def bernoulli(p):
    return stats.bernoulli.rvs(p)

def prob_busy(observation):
    # make a sample
    def sampling():
        cloudy = bernoulli(0.4)
        wind = bernoulli(0.8)
        exams = bernoulli(0.076)
        academic_holiday = bernoulli(0.26)

        rain = bernoulli(p_rain(wind, cloudy))
        event = bernoulli(p_event(exams))

        busy = bernoulli(p_busy(rain, event, academic_holiday))
        
        return {"cloudy":cloudy, "wind":wind, "exams":exams, "academic_holiday":academic_holiday, "rain":rain, "event":event, "busy":busy}
    
    def obs_match(output, obs):
        for key in obs.keys():
            if obs[key] != output[key]:
                return False
        return True
    
    samples = []
    busy = 0
    for iters in range(100000):
        sample = sampling()
        if obs_match(sample, observation):
            samples.append(sample)
            if sample["busy"] == 1:
                busy += 1
    
    return busy/len(samples)

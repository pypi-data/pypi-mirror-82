/* file "PhraseSpotterAPI.h" */

/* Copyright 2017 SoundHound, Incorporated.  All rights reserved. */

/*
   Public interface for Phrase Spotter library.
   This is primarily used for embedded solutions.
*/

#ifndef PHRASESPOTTERAPI_H
#define PHRASESPOTTERAPI_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * This method takes a single channel audio buffer containing 16 bit signed samples,
 * sampled at a rate of 16 KHz. It returns true (non-zero) if the target phrase was matched, false (zero) otherwise.
 *
 * samples - buffer containing 16 bit signed samples
 * num_samples - number of 16 bit samples contained in samples
 * pResult - Result code for operation, 0 for Success or an error code. Set to null if not interested.
 *
 */
int PhraseSpotterProcessSamples(int16_t *samples, uint32_t num_samples, int *pResult=NULL);

/**
 * Optional: After a phrase is spotted, PhraseSpotterGetLastSpottedScore() can be used to obtain
 * the score of the audio that trigged a hit.  This can be helpful when trying to adjust the
 * threshold to achieve the right balance between false positives and false negatives.
 * The threshold can be adjusted using PhraseSpotterSetThreshold, below.
 * The scores returned by PhraseSpotterGetLastSpottedScore are in the range [0..1]
 */
float PhraseSpotterGetLastSpottedScore();

/**
 * Use PhraseSpotterSetThreshold to adjust the sensitivity for phrase
 *   spotting.  Valid values are in the range [0..1]
 * With lower values the phrase spotter will trigger more frequently,
 *   capturing the wakeup phrase more often, but with increased chance
 *   for false positives.
 * Conversely, with higher values the phrase spotter will trigger less
 *   frequently, possibly missing the wakeup phrase more often, but
 *   with a lower false positive rate.
 * Use PhraseSpotterGetThreshold to obtain the current threshold setting.
 */
void PhraseSpotterSetThreshold(float threshold);
float PhraseSpotterGetThreshold();

#ifdef __cplusplus
} // extern
#endif

#endif

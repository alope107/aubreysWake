All examples run from this directory:

For text to speech:
```
python converter.py tts PATH/TO/PLAINTEXT PATH/TO/OUTPUT/DIRECTORY ../audio g2p_allos
```

If you're wanting to experiment with new phoneme recordings, __edit them in prebuild_assets__. Then run the resample. You can then run the tts command as many times as you like with the new samples.

```
python converter.py resample ../prebuild_assets/audio/man_phonemes/ ../audio
```
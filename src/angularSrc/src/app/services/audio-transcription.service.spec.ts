/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { AudioTranscriptionService } from './audio-transcription.service';

describe('Service: AudioTranscription', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AudioTranscriptionService]
    });
  });

  it('should ...', inject([AudioTranscriptionService], (service: AudioTranscriptionService) => {
    expect(service).toBeTruthy();
  }));
});

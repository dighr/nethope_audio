import { Component, OnInit } from '@angular/core';
import {AudioFileModel, AudioTranscriptionService} from '../../services/audio-transcription.service'

@Component({
  selector: 'app-audio-transcription',
  templateUrl: './audio-transcription.component.html',
  styleUrls: ['./audio-transcription.component.css'],
})
export class AudioTranscriptionComponent implements OnInit {

  audioFiles: AudioFileModel[] = [];
  constructor(private audioFileService: AudioTranscriptionService) { }

  ngOnInit() {
    this.getFiles()
  }

  getFiles() {
    this.audioFileService.getAllAudioFiles().subscribe(
      (resp: AudioFileModel[]) => {
        console.log(resp);
        this.audioFiles = resp;
      }
    )
  }

}

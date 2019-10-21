import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AudioTranscriptionService {

  baseUrl = 'http://127.0.0.1:8000'
  httpHeaders = new HttpHeaders({ 'Content-Type': 'application/json'})
  constructor(private http: HttpClient) { }

  getAllAudioFiles(): Observable<AudioFileModel[]> {
      return this.http.get<AudioFileModel[]>(this.baseUrl + '/audioFiles', {headers: this.httpHeaders})
  }

}

export class AudioFileModel {
    id: any;
    filename: any;
    timestamp: any;
    phonenumber: any;
    transcription: any;
    translation: any;
}

import pygame
class MusicPlayer:
    def __init__(self, playlist):
        self.playlist=playlist
        self.current_index=0
        self.is_playing=False

        pygame.mixer.init()
    
    def play(self):
        print("Trying to play:", self.playlist[self.current_index][0])
        pygame.mixer.music.load(self.playlist[self.current_index][0])
        pygame.mixer.music.play()
        self.is_playing=True
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing=False
    def next_track(self):
        self.current_index=(self.current_index+1)%len(self.playlist)
        self.play()
    def prev_track(self):
        self.current_index=(self.current_index-1)%len(self.playlist)
        self.play()
    def get_current_track(self):
        return self.playlist[self.current_index][0]
    def get_current_image(self):
        return self.playlist[self.current_index][1]
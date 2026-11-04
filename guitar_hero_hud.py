import pygame
import sys
import time
import wave
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LANE_WIDTH = 100
NUM_LANES = 4
LANE_POSITIONS = [SCREEN_WIDTH//2 - 1.5 * LANE_WIDTH + i * LANE_WIDTH for i in range(NUM_LANES)]
NOTE_SPEED = 4
NOTE_HEIGHT = 30
HIT_ZONE_Y = 500
HIT_TOLERANCE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
LANE_COLORS = [RED, GREEN, BLUE, YELLOW]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guitar Hero HUD - Pygame")

# Font
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

class Note:
    def __init__(self, lane, spawn_time):
        self.lane = lane
        self.spawn_time = spawn_time
        self.y = 0
        self.color = LANE_COLORS[lane]
        self.hit = False
        self.missed = False

    def update(self, dt):
        self.y += NOTE_SPEED

    def draw(self, surface):
        if not self.hit:
            x = LANE_POSITIONS[self.lane]
            pygame.draw.rect(surface, self.color, (x + 10, self.y, LANE_WIDTH - 40, NOTE_HEIGHT))
            pygame.draw.rect(surface, WHITE, (x + 10, self.y, LANE_WIDTH - 40, NOTE_HEIGHT), 2)

def load_wav_beats(filename="example.wav"):
    """Placeholder beat detection. Returns list of (time_in_seconds, lane)."""
    try:
        with wave.open(filename, 'rb') as wav:
            nframes = wav.getnframes()
            framerate = wav.getframerate()
            duration = nframes / float(framerate)
            print(f"Loaded {filename}: {duration:.1f}s, {nframes} frames")
        # Simple simulated pattern for demo
        beats = []
        t = 1.0
        while t < min(duration, 60):
            lane = random.randint(0, 3)
            beats.append((t, lane))
            t += random.choice([0.4, 0.5, 0.6, 0.8])
        return beats
    except Exception as e:
        print(f"WAV load failed ({e}), using simulated beats")
        return [(t, t % 4) for t in [i * 0.5 for i in range(40)]]

def main():
    clock = pygame.time.Clock()
    running = True
    notes = []
    score = 0
    combo = 0
    max_combo = 0
    misses = 0
    start_time = time.time()
    next_beat_idx = 0

    beats = load_wav_beats("example.wav")
    beats.sort(key=lambda x: x[0])

    # Optional: try to play the WAV if available
    try:
        pygame.mixer.music.load("example.wav")
        pygame.mixer.music.play(-1)
    except:
        print("No audio playback (example.wav missing or unsupported)")

    while running:
        dt = clock.tick(60) / 1000.0
        current_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                lane_keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
                for lane, key in enumerate(lane_keys):
                    if event.key == key:
                        # Check for hit
                        hit = False
                        for note in notes:
                            if not note.hit and note.lane == lane and abs(note.y - HIT_ZONE_Y) < HIT_TOLERANCE:
                                note.hit = True
                                score += 100 + combo * 10
                                combo += 1
                                max_combo = max(max_combo, combo)
                                hit = True
                                break
                        if not hit:
                            combo = 0
                            misses += 1

        # Spawn notes based on beat times
        while next_beat_idx < len(beats) and beats[next_beat_idx][0] <= current_time:
            _, lane = beats[next_beat_idx]
            notes.append(Note(lane, current_time))
            next_beat_idx += 1

        # Update notes
        for note in notes[:]:
            note.update(dt)
            if note.y > SCREEN_HEIGHT + 50:
                if not note.hit:
                    combo = 0
                    misses += 1
                notes.remove(note)

        # Draw
        screen.fill(BLACK)

        # Draw lanes and hit zone
        for i, x in enumerate(LANE_POSITIONS):
            pygame.draw.rect(screen, GRAY, (x, 0, LANE_WIDTH, SCREEN_HEIGHT), 2)
            pygame.draw.line(screen, GREEN, (x, HIT_ZONE_Y), (x + LANE_WIDTH, HIT_ZONE_Y), 4)
            # Lane labels
            label = small_font.render(["A", "S", "D", "F"][i], True, LANE_COLORS[i])
            screen.blit(label, (x + LANE_WIDTH//2 - 8, HIT_ZONE_Y + 10))

        # Draw notes
        for note in notes:
            note.draw(screen)

        # UI
        score_text = font.render(f"Score: {score}", True, WHITE)
        combo_text = font.render(f"Combo: {combo}", True, YELLOW if combo > 5 else WHITE)
        miss_text = small_font.render(f"Misses: {misses}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (10, 50))
        screen.blit(miss_text, (10, 90))

        # Instructions
        instr = small_font.render("Press A S D F to hit notes | Close window to quit", True, GRAY)
        screen.blit(instr, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

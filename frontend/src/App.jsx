import { useState, useRef, useEffect } from 'react'
import './App.css'

const DURATIONS = [0.1, 0.5, 2.0, 4.0, 8.0, 16.0];
const API_BASE = "https://dusiadle.onrender.com";

function App() {
  const [screen, setScreen] = useState('menu');
  const [songId, setSongId] = useState(null);
  const [currentCategory, setCurrentCategory] = useState(null); // Zapamiętujemy kategorię
  const [round, setRound] = useState(0);
  const [guess, setGuess] = useState('');
  const [feedback, setFeedback] = useState('');
  const audioRef = useRef(null);

  const [allSongs, setAllSongs] = useState([]);
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/songs`)
      .then(res => res.json())
      .then(data => setAllSongs(data))
      .catch(err => console.error(err));
  }, []);

  const startGame = async (category) => {
    setCurrentCategory(category);
    try {
      const res = await fetch(`${API_BASE}/api/random-song/${category}`);
      if (!res.ok) throw new Error("Brak piosenek");
      const data = await res.json();
      
      setSongId(data.song_id);
      setRound(0);
      setGuess('');
      setFeedback('');
      setShowSuggestions(false);
      setScreen('game');
    } catch (err) {
      alert("Błąd połączenia z backendem.");
    }
  };

  const playAudio = async () => {
    if (!songId) return;
    const currentDuration = DURATIONS[round];
    const audioUrl = `${API_BASE}/api/audio/${songId}?duration=${currentDuration}`;
    
    // Sprawdzamy, czy plik istnieje
    const checkRes = await fetch(audioUrl);
    
    if (checkRes.status === 404) {
      setFeedback("Szukam innej piosenki...");
      startGame(currentCategory); // Automatyczne losowanie ponownie!
      return;
    }

    if (audioRef.current) {
      audioRef.current.src = audioUrl;
      audioRef.current.play();
    }
  };

  const handleGuessChange = (e) => {
    const value = e.target.value;
    setGuess(value);

    if (value.length > 0) {
      const filtered = allSongs.filter(song => 
        song.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setGuess(suggestion);
    setShowSuggestions(false);
  };

  const handleSkip = async () => {
    setShowSuggestions(false);
    setGuess('');

    try {
      const res = await fetch(`${API_BASE}/api/guess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ song_id: songId, guess_text: '___skip___' })
      });
      const data = await res.json();

      if (round < DURATIONS.length - 1) {
        setRound(r => r + 1);
        setFeedback('Pominięto! Odblokowano dłuższy fragment.');
      } else {
        setFeedback(`Poddajesz się! To było: ${data.correct_artist} - ${data.correct_title}`);
        setScreen('end');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const submitGuess = async () => {
    if (!guess.trim()) return;
    setShowSuggestions(false);

    try {
      const res = await fetch(`${API_BASE}/api/guess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ song_id: songId, guess_text: guess })
      });
      const data = await res.json();

      if (data.correct) {
        setFeedback(`Brawo! To ${data.correct_artist} - ${data.correct_title}`);
        setScreen('end');
      } else {
        if (round < DURATIONS.length - 1) {
          setRound(r => r + 1);
          setGuess('');
          setFeedback('Pudło! Odblokowano dłuższy fragment.');
        } else {
          setFeedback(`Koniec prób! To było: ${data.correct_artist} - ${data.correct_title}`);
          setScreen('end');
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container">
      <h1>Dusiadle 🎵</h1>

      {screen === 'menu' && (
        <div className="menu">
          <p>Wybierz kategorię, aby zacząć:</p>
          <button onClick={() => startGame('hiphop')}>Hip-Hop</button>
          <button onClick={() => startGame('klasyki')}>Klasyki</button>
          <button onClick={() => startGame('popularne')}>Popularne</button>
        </div>
      )}

      {screen === 'game' && (
        <div className="game">
          <p>Próba {round + 1} z {DURATIONS.length}</p>
          <p>Aktualna długość: <strong>{DURATIONS[round]} sekundy</strong></p>
          
          <button className="play-btn" onClick={playAudio}>▶ Posłuchaj fragmentu</button>
          
          <div className="guess-section">
            <div className="autocomplete-wrapper">
              <input 
                type="text" 
                placeholder="Kto to śpiewa albo jaki to tytuł?" 
                value={guess}
                onChange={handleGuessChange}
                onKeyDown={(e) => e.key === 'Enter' && submitGuess()}
              />
              
              {showSuggestions && filteredSuggestions.length > 0 && (
                <ul className="suggestions-list">
                  {filteredSuggestions.map((song, index) => (
                    <li key={index} onClick={() => handleSuggestionClick(song)}>
                      {song}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="action-buttons">
              <button className="skip-btn" onClick={handleSkip}>Pomiń</button>
              <button className="submit-btn" onClick={submitGuess}>Zgaduję!</button>
            </div>
            
          </div>
          <p className="feedback">{feedback}</p>
        </div>
      )}

      {screen === 'end' && (
        <div className="end">
          <h2>{feedback}</h2>
          <button onClick={() => setScreen('menu')}>Zagraj ponownie</button>
        </div>
      )}

      <audio ref={audioRef} style={{ display: 'none' }} />
      <h1>Kocham Cię ❤️<hr></hr>Twój chłopak Karol</h1>
    </div>
    
  )
}

export default App
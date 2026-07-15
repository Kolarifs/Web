from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Инициализируем приложение FastAPI
app = FastAPI(title="LEEK_OS Music API", version="3.0.0")

# Настройка CORS, чтобы Android и iOS устройства могли делать запросы к серверу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Схемы валидации данных (Pydantic гарантирует строгость типов)
class TrackResponse(BaseModel):
    id: int
    title: str
    artist_name: str
    artist_id: str
    audio_url: str
    cover_url: str
    play_count: int

class ArtistResponse(BaseModel):
    id: str
    name: str
    avatar_url: str
    bio: str
    monthly_listeners: int

# База данных в оперативной памяти сервера (Mock DB слой)
DB_TRACKS = [
    {
        "id": 1,
        "title": "Cyber Evolution Protocol",
        "artist_name": "LEEKSEEK Engine",
        "artist_id": "art_1",
        "audio_url": "https://soundhelix.com",
        "cover_url": "https://picsum.photos",
        "play_count": 1250000,
    },
    {
        "id": 2,
        "title": "Quantum Shaders",
        "artist_name": "LEEKSEEK Engine",
        "artist_id": "art_1",
        "audio_url": "https://soundhelix.com",
        "cover_url": "https://picsum.photos",
        "play_count": 980000,
    },
    {
        "id": 3,
        "title": "Neon Impulse",
        "artist_name": "Sora Neon",
        "artist_id": "art_2",
        "audio_url": "https://soundhelix.com",
        "cover_url": "https://picsum.photos",
        "play_count": 2300000,
    }
]

DB_ARTISTS = {
    "art_1": {
        "id": "art_1",
        "name": "LEEKSEEK Engine",
        "avatar_url": "https://picsum.photos",
        "bio": "Разработчик низкоуровневых звуковых алгоритмов в среде LEEK_OS.",
        "monthly_listeners": 450000,
    },
    "art_2": {
        "id": "art_2",
        "name": "Sora Neon",
        "avatar_url": "https://picsum.photos",
        "bio": "Синтвейв-исполнитель, работающий с аппаратными текстурами звука.",
        "monthly_listeners": 890000,
    }
}

# --- МАРШРУТЫ API (ENDPOINTS) ---

@app.get("/api/v1/tracks/chart", response_model=List[TrackResponse])
async def get_chart():
    """Возвращает треки, автоматически отсортированные по числу воспроизведений (Чарт)"""
    sorted_tracks = sorted(DB_TRACKS, key=lambda x: x["play_count"], reverse=True)
    return sorted_tracks

@app.get("/api/v1/tracks/search", response_model=List[TrackResponse])
async def search_tracks(q: str = ""):
    """Быстрый поиск треков в базе данных по совпадению букв в названии или имени артиста"""
    if not q:
        return []
    query = q.lower()
    results = [
        t for t in DB_TRACKS
        if query in t["title"].lower() or query in t["artist_name"].lower()
    ]
    return results

@app.get("/api/v1/artists/{artist_id}", response_model=ArtistResponse)
async def get_artist(artist_id: str):
    """Получить карточку профиля конкретного исполнителя"""
    artist = DB_ARTISTS.get(artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Артист не найден в экосистеме LEEK_OS")
    return artist

@app.get("/api/v1/artists/{artist_id}/tracks", response_model=List[TrackResponse])
async def get_artist_tracks(artist_id: str):
    """Получить персональный список треков, принадлежащих только этому артисту"""
    return [t for t in DB_TRACKS if t["artist_id"] == artist_id]

if __name__ == "__main__":
    import uvicorn
    # ИСПРАВЛЕНО: Передаем строку "main:app" вместо объекта
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

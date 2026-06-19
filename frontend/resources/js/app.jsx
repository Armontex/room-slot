import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

function RoomSlotsRealtime({
  roomId,
  wsUrl,
  apiUrl,
  initialSlots,
  bookingUrl,
  csrfToken,
}) {
  const [slotsSchedule, setSlotsSchedule] = useState(initialSlots);
  const [error, setError] = useState(null);

  async function reloadSlots() {
    const response = await fetch(`${apiUrl}/rooms/${roomId}/slots`, {
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to load slots');
    }

    setSlotsSchedule(await response.json());
  }

  useEffect(() => {
    const socket = new WebSocket(`${wsUrl}/ws/rooms/${roomId}`);

    socket.addEventListener('message', async () => {
      try {
        await reloadSlots();
      } catch {
        setError('Failed to refresh slots');
      }
    });

    return () => {
      socket.close();
    };
  }, [roomId, wsUrl, apiUrl]);

  if (!slotsSchedule) {
    return null;
  }

  return (
    <section>
      <h2>Слоты</h2>

      {error && <p>{error}</p>}

      <p>
        Период: с {slotsSchedule.date_from} по {slotsSchedule.date_to}
      </p>

      {slotsSchedule.days.map((day) => (
        <section key={day.date}>
          <h3>{day.date}</h3>

          {day.slots.length === 0 ? (
            <p>Слотов нет.</p>
          ) : (
            <ul>
              {day.slots.map((slot) => (
                <li key={`${day.date}-${slot.time}`}>
                  <span>{slot.time.slice(0, 5)}</span>{' '}

                  {slot.status === 'available' ? (
                    <>
                      <span>Свободно</span>

                      <form method="POST" action={bookingUrl}>
                        <input type="hidden" name="_token" value={csrfToken} />
                        <input type="hidden" name="room_id" value={roomId} />
                        <input type="hidden" name="date" value={day.date} />
                        <input type="hidden" name="start_time" value={slot.time} />

                        <button type="submit">Забронировать</button>
                      </form>
                    </>
                  ) : slot.status === 'booked' ? (
                    <span>Занято</span>
                  ) : slot.status === 'past' ? (
                    <span>Прошло</span>
                  ) : (
                    <span>{slot.status}</span>
                  )}
                </li>
              ))}
            </ul>
          )}
        </section>
      ))}
    </section>
  );
}

const root = document.getElementById('room-slots-root');

if (root) {
  createRoot(root).render(
    <RoomSlotsRealtime
      roomId={root.dataset.roomId}
      wsUrl={root.dataset.wsUrl}
      apiUrl={root.dataset.apiUrl}
      initialSlots={JSON.parse(root.dataset.initialSlots)}
      bookingUrl={root.dataset.bookingUrl}
      csrfToken={root.dataset.csrfToken}
    />,
  );
}

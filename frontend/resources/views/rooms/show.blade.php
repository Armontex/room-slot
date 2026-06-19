@extends('layouts.app')

@section('content')
  <a href="{{ route('rooms.index') }}">Назад к комнатам</a>

  @if ($error)
    <p>{{ $error }}</p>
  @endif

  @if ($room)
    <h1>{{ $room['name'] }}</h1>

    <div>
      <span>Здание</span>
      <span>{{ $room['building'] }}</span>
    </div>

    <div>
      <span>Этаж</span>
      <span>{{ $room['floor'] }}</span>
    </div>

    <div>
      <span>Мест</span>
      <span>{{ $room['capacity'] }}</span>
    </div>

    @if (!empty($room['description']))
      <div>
        <span>Описание</span>
        <span>{{ $room['description'] }}</span>
      </div>
    @endif
  @endif

  @if ($slotsSchedule)
    <h2>Слоты</h2>

    <p>
      Период:
      {{ $slotsSchedule['date_from'] }}
      —
      {{ $slotsSchedule['date_to'] }}
    </p>

    @foreach ($slotsSchedule['days'] as $day)
      <section>
        <h3>{{ $day['date'] }}</h3>

        @if (empty($day['slots']))
          <p>Слотов нет.</p>
        @else
          <ul>
            @foreach ($day['slots'] as $slot)
              <li>
                <span>{{ substr($slot['time'], 0, 5) }}</span>
                @if ($slot['status'] === 'available')
                  <span>Свободно</span>
                @elseif ($slot['status'] === 'booked')
                  <span>Занято</span>
                @elseif ($slot['status'] === 'past')
                  <span>Прошло</span>
                @else
                  <span>{{ $slot['status'] }}</span>
                @endif
              </li>
            @endforeach
          </ul>
        @endif
      </section>
    @endforeach
  @endif
@endsection

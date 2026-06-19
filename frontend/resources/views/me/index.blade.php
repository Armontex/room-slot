@extends('layouts.app')

@section('content')
  <h1>Мои бронирования</h1>

  @if ($error)
    <p>{{ $error }}</p>
  @endif

  @if ($errors->has('booking'))
    <p>{{ $errors->first('booking') }}</p>
  @endif

  @if ($user)
    <section>
      <h2>Профиль</h2>

      <div>
        <span>Email</span>
        <span>{{ $user['email'] }}</span>
      </div>

      <div>
        <span>Роль</span>
        <span>{{ $user['role'] }}</span>
      </div>
    </section>
  @endif

  <section>
    <h2>Брони</h2>

    @if (empty($bookings))
      <p>Бронирований пока нет.</p>
    @else
      <p>Всего бронирований: {{ $total }}</p>

      <ul>
        @foreach ($bookings as $booking)
          <li>
            <div>
              <span>Комната</span>
              <a href="{{ route('rooms.show', ['roomId' => $booking['room_id']]) }}">
                {{ $booking['room_id'] }}
              </a>
            </div>

            <div>
              <span>Дата</span>
              <span>{{ $booking['slot']['date'] }}</span>
            </div>

            <div>
              <span>Время</span>
              <span>{{ substr($booking['slot']['start_time'], 0, 5) }}</span>
            </div>

            <div>
              <span>Статус</span>
              <span>{{ $booking['status'] }}</span>
            </div>

            <div>
              <span>Создано</span>
              <span>{{ $booking['created_at'] }}</span>
            </div>

            @if ($booking['status'] === 'active')
              <form method="POST" action="{{ route('bookings.cancel', ['bookingId' => $booking['id']]) }}">
                @csrf
                <button type="submit">Отменить</button>
              </form>
            @endif

            @if (!empty($booking['cancelled_at']))
              <div>
                <span>Отменено</span>
                <span>{{ $booking['cancelled_at'] }}</span>
              </div>
            @endif
          </li>
        @endforeach
      </ul>
    @endif
  </section>
@endsection

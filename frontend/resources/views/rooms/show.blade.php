@extends('layouts.app')

@section('content')
  <a href="{{ route('rooms.index') }}">Назад к комнатам</a>

  @if ($error)
    <p>{{ $error }}</p>
  @endif

  @if ($errors->has('booking'))
    <p>{{ $errors->first('booking') }}</p>
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
    <div
      id="room-slots-root"
      data-room-id="{{ $room['id'] }}"
      data-ws-url="{{ config('services.fastapi.ws_url') }}"
      data-api-url="{{ config('services.fastapi.browser_url') }}"
      data-initial-slots='@json($slotsSchedule)'
      data-booking-url="{{ route('bookings.store') }}"
      data-csrf-token="{{ csrf_token() }}"
    ></div>
  @endif
@endsection

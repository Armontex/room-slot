@extends('layouts.app')

@section('content')
    <h1>Комнаты</h1>

    @if ($error)
        <p>{{ $error }}</p>
    @endif

    @if (empty($rooms))
        <p>Комнаты не найдены.</p>
    @else
        <p>Всего комнат: {{ $total }}</p>
        <ul>
            @foreach ($rooms as $room)
                <li>
                    <h2>{{ $room['name'] }}</h2>

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

                    <a href="/rooms/{{ $room['id'] }}">Открыть</a>
                </li>
            @endforeach
        </ul>
    @endif

@endsection

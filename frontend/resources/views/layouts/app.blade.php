<!DOCTYPE html>
<html lang="ru">

<head>
  <meta charset="utf-8">
  <title>{{ $title ?? 'RoomSlot' }}</title>
  @vite(['resources/css/app.css', 'resources/js/app.jsx'])
</head>

<body>
  <header>
    <a href="{{ route('rooms.index') }}">RoomSlot</a>

    @if (session('access_token'))
      <nav>
        <a href="{{ route('rooms.index') }}">Комнаты</a>
        <a href="{{ route('me.index') }}">Мои бронирования</a>
      </nav>

      <form method="POST" action="{{ route('logout') }}">
        @csrf
        <button type="submit">Выйти</button>
      </form>
    @endif
  </header>
  <main>
    @yield('content')
  </main>
</body>

</html>

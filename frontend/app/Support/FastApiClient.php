<?php

namespace App\Support;

use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Support\Facades\Http;

final class FastApiClient
{
    public function get(string $path, array $query = [], ?string $token = null): Response
    {
        return $this->request($token)->get($path, $query);
    }

    public function post(string $path, array $data = [], ?string $token = null): Response
    {
        return $this->request($token)->post($path, $data);
    }

    private function request(?string $token = null): PendingRequest
    {
        $request = Http::baseUrl(config('services.fastapi.url'))
            ->acceptJson()
            ->asJson()
            ->timeout(5);

        if ($token !== null) {
            $request = $request->withToken($token);
        }
        return $request;
    }
}

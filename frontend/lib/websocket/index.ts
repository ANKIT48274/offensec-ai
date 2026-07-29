"use client";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

type MessageHandler = (_data: any) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();

  connect(assessmentId: string) {
    if (this.ws?.readyState === WebSocket.OPEN) return;

    this.ws = new WebSocket(WS_URL);

    this.ws.onopen = () => {
      this.ws?.send(JSON.stringify({ type: "subscribe", assessment_id: assessmentId }));
    };

    this.ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        const type = parsed.type || "message";
        const handlers = this.handlers.get(type);
        if (handlers) handlers.forEach((h) => h(parsed));
      } catch {
        // ignore
      }
    };

    this.ws.onclose = () => {
      setTimeout(() => this.connect(assessmentId), 3000);
    };
  }

  disconnect() {
    this.ws?.close();
    this.ws = null;
  }

  on(event: string, handler: MessageHandler) {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler);
  }

  off(event: string, handler: MessageHandler) {
    this.handlers.get(event)?.delete(handler);
  }
}

export const wsClient = new WebSocketClient();

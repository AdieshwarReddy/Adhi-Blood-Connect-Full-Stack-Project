import { useState, useRef, useEffect } from "react";
import { MessageCircle, X, Send, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { ChatAPI } from "@/services/api";

interface Msg { role: "user" | "bot"; text: string }

export function Chatbot() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Msg[]>([
    { role: "bot", text: "Hi! I'm Adhi AI. Ask me anything about blood donation — eligibility, process, or benefits." },
  ]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, open]);

  const send = async () => {
    if (!input.trim()) return;
    const q = input.trim();
    setMessages((m) => [...m, { role: "user", text: q }]);
    setInput("");
    
    // Add temporary loading indicator
    setMessages((m) => [...m, { role: "bot", text: "..." }]);
    
    try {
      const res = await ChatAPI.ask(q);
      const reply = res.data.data?.reply || res.data.data || "I couldn't generate a response.";
      setMessages((m) => {
        const filtered = m.slice(0, -1);
        return [...filtered, { role: "bot", text: reply }];
      });
    } catch (error) {
      setMessages((m) => {
        const filtered = m.slice(0, -1);
        return [...filtered, { role: "bot", text: "Sorry, I couldn't reach the medical AI service right now. Please try again later." }];
      });
    }
  };

  return (
    <>
      <button
        onClick={() => setOpen((o) => !o)}
        className="fixed bottom-6 right-6 z-50 grid h-14 w-14 place-items-center rounded-full bg-primary-gradient text-primary-foreground shadow-elevated transition hover:scale-105 animate-pulse-ring"
        aria-label="Open chat"
      >
        {open ? <X className="h-6 w-6" /> : <MessageCircle className="h-6 w-6" />}
      </button>

      <div
        className={cn(
          "fixed bottom-24 right-6 z-50 flex w-[calc(100vw-3rem)] max-w-sm flex-col rounded-2xl border bg-card shadow-elevated transition-all sm:w-96",
          open ? "pointer-events-auto translate-y-0 opacity-100" : "pointer-events-none translate-y-4 opacity-0",
        )}
      >
        <div className="flex items-center gap-3 border-b p-4">
          <div className="grid h-9 w-9 place-items-center rounded-full bg-primary-gradient text-primary-foreground">
            <Bot className="h-4 w-4" />
          </div>
          <div>
            <p className="text-sm font-semibold">Adhi AI Assistant</p>
            <p className="text-xs text-success">● Online</p>
          </div>
        </div>
        <div ref={scrollRef} className="h-80 space-y-3 overflow-y-auto p-4">
          {messages.map((m, i) => (
            <div key={i} className={cn("flex", m.role === "user" ? "justify-end" : "justify-start")}>
              <div
                className={cn(
                  "max-w-[80%] rounded-2xl px-3 py-2 text-sm",
                  m.role === "user"
                    ? "rounded-br-sm bg-primary text-primary-foreground"
                    : "rounded-bl-sm bg-muted text-foreground",
                )}
              >
                {m.text}
              </div>
            </div>
          ))}
        </div>
        <div className="border-t p-3">
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Ask about donation..."
            />
            <Button size="icon" onClick={send} className="shrink-0 bg-primary-gradient">
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}

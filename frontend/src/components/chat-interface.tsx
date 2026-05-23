'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { useChatStore } from '@/lib/store'
import { sendChatMessage, createChatSession } from '@/lib/api'
import { cn } from '@/lib/utils'

interface ChatInterfaceProps {
  repositoryId: string
}

export function ChatInterface({ repositoryId }: ChatInterfaceProps) {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const { sessionId, setSessionId, messages, addMessage } = useChatStore()

  useEffect(() => {
    // Create chat session on mount
    if (!sessionId) {
      createChatSession(repositoryId).then((data) => {
        setSessionId(data.session_id)
      })
    }
  }, [repositoryId, sessionId, setSessionId])

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || !sessionId || loading) return

    const userMessage = input.trim()
    setInput('')
    addMessage({ role: 'user', content: userMessage })
    setLoading(true)

    try {
      const response = await sendChatMessage(sessionId, userMessage)
      addMessage({
        role: 'assistant',
        content: response.content,
        sources: response.sources,
      })
    } catch (error) {
      console.error('Failed to send message:', error)
      addMessage({
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your message.',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground py-8">
            <p className="text-lg mb-2">👋 Hi! I'm your AI assistant</p>
            <p className="text-sm">Ask me anything about this repository</p>
            <div className="mt-4 space-y-2">
              <p className="text-xs">Try asking:</p>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => setInput('How does authentication work?')}
                  className="text-xs text-primary hover:underline"
                >
                  "How does authentication work?"
                </button>
                <button
                  onClick={() => setInput('Explain the project structure')}
                  className="text-xs text-primary hover:underline"
                >
                  "Explain the project structure"
                </button>
                <button
                  onClick={() => setInput('How do I run this project?')}
                  className="text-xs text-primary hover:underline"
                >
                  "How do I run this project?"
                </button>
              </div>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={cn(
              'flex',
              message.role === 'user' ? 'justify-end' : 'justify-start'
            )}
          >
            <div
              className={cn(
                'max-w-[80%] rounded-lg px-4 py-2',
                message.role === 'user'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted'
              )}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              {message.sources && message.sources.length > 0 && (
                <div className="mt-2 pt-2 border-t border-border/50">
                  <p className="text-xs text-muted-foreground mb-1">Sources:</p>
                  {message.sources.map((source, idx) => (
                    <p key={idx} className="text-xs text-muted-foreground">
                      📄 {source.file}
                    </p>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-muted rounded-lg px-4 py-2">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about the codebase..."
            disabled={loading || !sessionId}
          />
          <Button
            onClick={handleSend}
            disabled={loading || !sessionId || !input.trim()}
            size="icon"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}

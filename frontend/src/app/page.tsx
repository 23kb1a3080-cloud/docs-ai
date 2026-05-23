'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Github, Sparkles, FileText, MessageSquare, GitPullRequest } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useRepositoryStore } from '@/lib/store'
import { analyzeRepository } from '@/lib/api'

export default function Home() {
  const router = useRouter()
  const [githubUrl, setGithubUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const setCurrentRepository = useRepositoryStore((state) => state.setCurrentRepository)

  const handleAnalyze = async () => {
    if (!githubUrl) {
      setError('Please enter a GitHub URL')
      return
    }

    setLoading(true)
    setError('')

    try {
      const repository = await analyzeRepository(githubUrl)
      setCurrentRepository(repository)
      router.push(`/dashboard/${repository.id}`)
    } catch (err: any) {
      setError(err.message || 'Failed to analyze repository')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12 animate-fade-in">
          <div className="flex items-center justify-center mb-6">
            <Sparkles className="w-12 h-12 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            DocMind AI
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-2">
            Self-Updating Developer Knowledge Agent
          </p>
          <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
            Transform your GitHub repository into a living knowledge system with AI-powered documentation
          </p>
        </div>

        {/* Input Section */}
        <div className="max-w-3xl mx-auto mb-16 animate-slide-in">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
            <div className="flex items-center gap-2 mb-4">
              <Github className="w-6 h-6 text-gray-600 dark:text-gray-300" />
              <h2 className="text-2xl font-semibold">Analyze Your Repository</h2>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Enter a public GitHub repository URL to get started
            </p>
            <div className="flex gap-3">
              <Input
                type="text"
                placeholder="https://github.com/owner/repository"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                className="flex-1 h-12 text-lg"
                disabled={loading}
              />
              <Button
                onClick={handleAnalyze}
                disabled={loading}
                className="h-12 px-8 text-lg"
              >
                {loading ? 'Analyzing...' : 'Analyze'}
              </Button>
            </div>
            {error && (
              <p className="text-red-500 mt-3 text-sm">{error}</p>
            )}
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          <FeatureCard
            icon={<FileText className="w-8 h-8" />}
            title="Auto Documentation"
            description="Generate comprehensive docs automatically from your codebase"
          />
          <FeatureCard
            icon={<GitPullRequest className="w-8 h-8" />}
            title="PR Analysis"
            description="Analyze pull requests and suggest documentation updates"
          />
          <FeatureCard
            icon={<MessageSquare className="w-8 h-8" />}
            title="AI Chat Assistant"
            description="Ask questions about your codebase and get instant answers"
          />
          <FeatureCard
            icon={<Sparkles className="w-8 h-8" />}
            title="Smart Updates"
            description="Automatically update docs when code changes"
          />
        </div>

        {/* Example Section */}
        <div className="mt-16 text-center">
          <p className="text-gray-600 dark:text-gray-400 mb-4">Try with an example:</p>
          <div className="flex flex-wrap justify-center gap-3">
            <Button
              variant="outline"
              onClick={() => setGithubUrl('https://github.com/fastapi/fastapi')}
            >
              FastAPI
            </Button>
            <Button
              variant="outline"
              onClick={() => setGithubUrl('https://github.com/vercel/next.js')}
            >
              Next.js
            </Button>
            <Button
              variant="outline"
              onClick={() => setGithubUrl('https://github.com/facebook/react')}
            >
              React
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
      <div className="text-blue-600 dark:text-blue-400 mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 text-sm">{description}</p>
    </div>
  )
}

'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import {
  FileText,
  GitBranch,
  MessageSquare,
  Settings,
  Loader2,
  FolderTree,
  BookOpen,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { MarkdownViewer } from '@/components/markdown-viewer'
import { ChatInterface } from '@/components/chat-interface'
import {
  getRepository,
  getRepositoryStructure,
  listDocumentation,
  getDocumentation,
  generateDocumentation,
} from '@/lib/api'
import { cn } from '@/lib/utils'

export default function DashboardPage() {
  const params = useParams()
  const repositoryId = params.id as string

  const [selectedDoc, setSelectedDoc] = useState<string>('readme')
  const [showChat, setShowChat] = useState(false)
  const [generating, setGenerating] = useState(false)

  // Fetch repository
  const { data: repository, isLoading: repoLoading } = useQuery({
    queryKey: ['repository', repositoryId],
    queryFn: () => getRepository(repositoryId),
  })

  // Fetch repository structure
  const { data: structure } = useQuery({
    queryKey: ['structure', repositoryId],
    queryFn: () => getRepositoryStructure(repositoryId),
    enabled: !!repository,
  })

  // Fetch documentation list
  const { data: docList, refetch: refetchDocs } = useQuery({
    queryKey: ['documentation-list', repositoryId],
    queryFn: () => listDocumentation(repositoryId),
    enabled: !!repository,
  })

  // Fetch selected documentation
  const { data: documentation, isLoading: docLoading } = useQuery({
    queryKey: ['documentation', repositoryId, selectedDoc],
    queryFn: () => getDocumentation(repositoryId, selectedDoc),
    enabled: !!repository && !!selectedDoc,
  })

  const handleGenerateDocs = async () => {
    setGenerating(true)
    try {
      await generateDocumentation(repositoryId, ['readme', 'api', 'architecture', 'setup'])
      await refetchDocs()
    } catch (error) {
      console.error('Failed to generate documentation:', error)
    } finally {
      setGenerating(false)
    }
  }

  if (repoLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    )
  }

  if (!repository) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Repository not found</p>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Left Sidebar - File Tree */}
      <div className="w-64 border-r bg-card overflow-y-auto">
        <div className="p-4 border-b">
          <h2 className="font-semibold text-lg truncate">{repository.name}</h2>
          <p className="text-sm text-muted-foreground truncate">{repository.owner}</p>
        </div>

        <div className="p-4">
          <div className="flex items-center gap-2 mb-3">
            <FolderTree className="w-4 h-4" />
            <h3 className="font-medium text-sm">Repository Files</h3>
          </div>
          <div className="space-y-1 text-sm">
            {structure?.tree?.slice(0, 20).map((item: any, idx: number) => (
              <div key={idx} className="py-1 px-2 hover:bg-accent rounded cursor-pointer truncate">
                {item.path}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Center Panel - Documentation */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <div className="border-b bg-card p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <BookOpen className="w-5 h-5" />
              <h1 className="text-xl font-semibold">Documentation</h1>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleGenerateDocs}
                disabled={generating}
              >
                {generating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  'Generate Docs'
                )}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowChat(!showChat)}
              >
                <MessageSquare className="w-4 h-4 mr-2" />
                {showChat ? 'Hide Chat' : 'Show Chat'}
              </Button>
            </div>
          </div>

          {/* Doc Type Tabs */}
          <div className="flex gap-2 mt-4">
            {['readme', 'api', 'architecture', 'setup'].map((type) => (
              <Button
                key={type}
                variant={selectedDoc === type ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedDoc(type)}
              >
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </Button>
            ))}
          </div>
        </div>

        {/* Documentation Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {docLoading ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="w-8 h-8 animate-spin" />
            </div>
          ) : documentation ? (
            <MarkdownViewer content={documentation.content} />
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <FileText className="w-16 h-16 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No Documentation Yet</h3>
              <p className="text-muted-foreground mb-4">
                Generate documentation to get started
              </p>
              <Button onClick={handleGenerateDocs} disabled={generating}>
                {generating ? 'Generating...' : 'Generate Documentation'}
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Right Sidebar - Chat */}
      {showChat && (
        <div className="w-96 border-l bg-card flex flex-col">
          <div className="p-4 border-b">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              <h2 className="font-semibold">AI Assistant</h2>
            </div>
          </div>
          <div className="flex-1 overflow-hidden">
            <ChatInterface repositoryId={repositoryId} />
          </div>
        </div>
      )}
    </div>
  )
}

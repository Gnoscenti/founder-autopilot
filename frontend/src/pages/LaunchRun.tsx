import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { Play, Rocket, CheckCircle, Circle, AlertCircle, Loader } from 'lucide-react'
import { createRun, getRun, getRunTasks, executeNextTask } from '../lib/api'

export default function LaunchRun() {
  const [goal, setGoal] = useState('Launch a $10k/month SaaS business')
  const [currentRunId, setCurrentRunId] = useState<string | null>(null)

  const createRunMutation = useMutation({
    mutationFn: createRun,
    onSuccess: (data) => {
      setCurrentRunId(data.run_id)
    },
  })

  const executeTaskMutation = useMutation({
    mutationFn: executeNextTask,
  })

  const { data: runData, refetch: refetchRun } = useQuery({
    queryKey: ['run', currentRunId],
    queryFn: () => getRun(currentRunId!),
    enabled: !!currentRunId,
    refetchInterval: 5000, // Poll every 5 seconds
  })

  const { data: tasksData } = useQuery({
    queryKey: ['runTasks', currentRunId],
    queryFn: () => getRunTasks(currentRunId!),
    enabled: !!currentRunId,
    refetchInterval: 5000,
  })

  const handleLaunch = () => {
    const spec = localStorage.getItem('businessSpec')
    const constraints = spec ? JSON.parse(spec) : {}

    createRunMutation.mutate({
      goal,
      constraints,
    })
  }

  const handleExecuteNext = () => {
    if (currentRunId) {
      executeTaskMutation.mutate(currentRunId, {
        onSuccess: () => {
          refetchRun()
        },
      })
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="text-green-500" size={20} />
      case 'running':
        return <Loader className="text-blue-500 animate-spin" size={20} />
      case 'failed':
        return <AlertCircle className="text-red-500" size={20} />
      default:
        return <Circle className="text-gray-300" size={20} />
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Launch Run</h1>
        <p className="mt-2 text-gray-600">
          Start a new business building run with the orchestrator
        </p>
      </div>

      {!currentRunId ? (
        <div className="card space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Business Goal
            </label>
            <textarea
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              rows={3}
              placeholder="Describe your business goal..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <button
            onClick={handleLaunch}
            disabled={createRunMutation.isPending}
            className="btn btn-primary flex items-center gap-2"
          >
            <Rocket size={16} />
            {createRunMutation.isPending ? 'Launching...' : 'Launch Run'}
          </button>

          {createRunMutation.isError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
              Error launching run. Please try again.
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-6">
          {/* Run Status */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Run Status</h2>
                <p className="text-sm text-gray-500">ID: {currentRunId}</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-primary-600">
                  {Math.round((runData?.progress || 0) * 100)}%
                </div>
                <div className="text-sm text-gray-500">{runData?.status}</div>
              </div>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all"
                style={{ width: `${(runData?.progress || 0) * 100}%` }}
              />
            </div>

            <div className="mt-4">
              <button
                onClick={handleExecuteNext}
                disabled={executeTaskMutation.isPending || runData?.status === 'completed'}
                className="btn btn-primary flex items-center gap-2"
              >
                <Play size={16} />
                {executeTaskMutation.isPending ? 'Executing...' : 'Execute Next Task'}
              </button>
            </div>
          </div>

          {/* Tasks List */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Tasks</h2>
            <div className="space-y-3">
              {tasksData?.tasks.map((task) => (
                <div
                  key={task.id}
                  className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
                >
                  {getStatusIcon(task.status)}
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{task.title}</div>
                    <div className="text-sm text-gray-500">
                      {task.type} • Agent: {task.agent}
                    </div>
                  </div>
                  <div className="text-xs font-medium px-2 py-1 rounded bg-gray-200 text-gray-700">
                    {task.status}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

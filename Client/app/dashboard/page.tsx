import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Bot, MessageSquare, Users, Plus } from "lucide-react"
import { TenantPageHeader } from "@/components/tenant-page-header"
import { TenantMetricCard } from "@/components/tenant-metric-card"
import { TenantChatbotList } from "@/components/tenant-chatbot-list"
import { TenantConversationChart } from "@/components/tenant-conversation-chart"

export default function TenantDashboardPage() {
  return (
    <div className="flex flex-col">
      <TenantPageHeader
        title="Dashboard"
        description="Overview of your chatbots and interactions"
        actions={
          <Button size="sm">
            <Plus className="mr-2 h-4 w-4" />
            New Chatbot
          </Button>
        }
      />

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <TenantMetricCard
          title="Active Chatbots"
          value="3"
          description="2 published, 1 draft"
          icon={<Bot className="h-4 w-4 text-muted-foreground" />}
        />
        <TenantMetricCard
          title="Total Conversations"
          value="1,284"
          description="+24% from last month"
          icon={<MessageSquare className="h-4 w-4 text-muted-foreground" />}
          trend="up"
        />
        <TenantMetricCard
          title="Unique Users"
          value="842"
          description="+18% from last month"
          icon={<Users className="h-4 w-4 text-muted-foreground" />}
          trend="up"
        />
      </div>

      <Tabs defaultValue="overview" className="mt-6">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="chatbots">Chatbots</TabsTrigger>
          <TabsTrigger value="conversations">Conversations</TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            <Card className="lg:col-span-4">
              <CardHeader>
                <CardTitle>Conversation Activity</CardTitle>
                <CardDescription>Daily chatbot interactions</CardDescription>
              </CardHeader>
              <CardContent className="pl-2">
                <TenantConversationChart />
              </CardContent>
            </Card>
            <Card className="lg:col-span-3">
              <CardHeader>
                <CardTitle>Your Chatbots</CardTitle>
                <CardDescription>Manage your active chatbots</CardDescription>
              </CardHeader>
              <CardContent>
                <TenantChatbotList limit={3} />
              </CardContent>
            </Card>
          </div>
        </TabsContent>
        <TabsContent value="chatbots">
          <Card>
            <CardHeader>
              <CardTitle>All Chatbots</CardTitle>
              <CardDescription>Manage all your chatbots</CardDescription>
            </CardHeader>
            <CardContent>
              <TenantChatbotList />
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="conversations">
          <Card>
            <CardHeader>
              <CardTitle>Conversation Analytics</CardTitle>
              <CardDescription>Detailed view of chatbot interactions</CardDescription>
            </CardHeader>
            <CardContent>
              <TenantConversationChart />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

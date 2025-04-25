import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { TenantPageHeader } from "@/components/tenant-page-header"
import { ChatbotTemplateSelector } from "@/components/chatbot-template-selector"
import { ChatbotPreview } from "@/components/chatbot-preview"

export default function CreateChatbotPage() {
  return (
    <div className="flex flex-col">
      <TenantPageHeader title="Create Chatbot" description="Configure and deploy a new chatbot" />

      <Tabs defaultValue="basic" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="basic">Basic Info</TabsTrigger>
          <TabsTrigger value="appearance">Appearance</TabsTrigger>
          <TabsTrigger value="behavior">Behavior</TabsTrigger>
          <TabsTrigger value="preview">Preview</TabsTrigger>
        </TabsList>

        <TabsContent value="basic" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>Configure the basic settings for your chatbot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="chatbot-name">Chatbot Name</Label>
                <Input id="chatbot-name" placeholder="Customer Support Bot" />
                <p className="text-xs text-muted-foreground">This name will be displayed to your users</p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="chatbot-description">Description</Label>
                <Textarea
                  id="chatbot-description"
                  placeholder="A helpful assistant for customer support inquiries..."
                  className="min-h-[100px]"
                />
                <p className="text-xs text-muted-foreground">Brief description of your chatbot's purpose</p>
              </div>
              <div className="space-y-2">
                <Label>Start from Template</Label>
                <ChatbotTemplateSelector />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save & Continue</Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Data Sources</CardTitle>
              <CardDescription>Select data sources to power your chatbot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-md border">
                <div className="grid grid-cols-12 gap-4 p-4 text-sm font-medium text-muted-foreground">
                  <div className="col-span-1"></div>
                  <div className="col-span-5">Source</div>
                  <div className="col-span-3">Type</div>
                  <div className="col-span-3">Last Updated</div>
                </div>
                {[
                  {
                    id: "1",
                    name: "Company FAQ",
                    type: "manual",
                    lastUpdated: "2023-08-12T00:00:00.000Z",
                  },
                  {
                    id: "2",
                    name: "Product Catalog",
                    type: "manual",
                    lastUpdated: "2023-09-05T00:00:00.000Z",
                  },
                  {
                    id: "3",
                    name: "Company Handbook.pdf",
                    type: "file",
                    lastUpdated: "2023-07-22T00:00:00.000Z",
                  },
                ].map((source) => (
                  <div key={source.id} className="grid grid-cols-12 gap-4 border-t p-4 text-sm">
                    <div className="col-span-1 flex items-center">
                      <Switch id={`source-${source.id}`} />
                    </div>
                    <div className="col-span-5 flex items-center">
                      <Label htmlFor={`source-${source.id}`} className="font-medium">
                        {source.name}
                      </Label>
                    </div>
                    <div className="col-span-3 flex items-center capitalize">{source.type}</div>
                    <div className="col-span-3 flex items-center">
                      {new Date(source.lastUpdated).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Manage Data Sources</Button>
              <Button>Save & Continue</Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="appearance" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Appearance</CardTitle>
              <CardDescription>Customize how your chatbot looks</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="primary-color">Primary Color</Label>
                  <div className="flex gap-2">
                    <Input id="primary-color" type="color" className="w-12 p-1" defaultValue="#0070f3" />
                    <Input defaultValue="#0070f3" className="font-mono" />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="secondary-color">Secondary Color</Label>
                  <div className="flex gap-2">
                    <Input id="secondary-color" type="color" className="w-12 p-1" defaultValue="#f5f5f5" />
                    <Input defaultValue="#f5f5f5" className="font-mono" />
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="chatbot-avatar">Chatbot Avatar</Label>
                <div className="flex items-center gap-4">
                  <div className="h-16 w-16 rounded-full bg-primary flex items-center justify-center text-primary-foreground text-2xl font-bold">
                    AI
                  </div>
                  <Button variant="outline" size="sm">
                    Upload Image
                  </Button>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="welcome-message">Welcome Message</Label>
                <Textarea
                  id="welcome-message"
                  placeholder="Hi there! How can I help you today?"
                  className="min-h-[100px]"
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="show-branding">Show Branding</Label>
                  <Switch id="show-branding" defaultChecked />
                </div>
                <p className="text-xs text-muted-foreground">
                  Display "Powered by ChatBotSaaS" in the chatbot interface
                </p>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save & Continue</Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="behavior" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Behavior Settings</CardTitle>
              <CardDescription>Configure how your chatbot interacts with users</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="auto-show">Auto-show Chatbot</Label>
                  <Switch id="auto-show" />
                </div>
                <p className="text-xs text-muted-foreground">Automatically open the chatbot after page load</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="delay-time">Delay Time (seconds)</Label>
                <Input id="delay-time" type="number" min="0" defaultValue="5" />
                <p className="text-xs text-muted-foreground">Time to wait before showing the chatbot automatically</p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="collect-email">Collect User Email</Label>
                  <Switch id="collect-email" defaultChecked />
                </div>
                <p className="text-xs text-muted-foreground">
                  Ask users for their email before starting a conversation
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="fallback-contact">Fallback to Contact Form</Label>
                  <Switch id="fallback-contact" defaultChecked />
                </div>
                <p className="text-xs text-muted-foreground">
                  Show a contact form when the chatbot can't answer a question
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="fallback-message">Fallback Message</Label>
                <Textarea
                  id="fallback-message"
                  placeholder="I'm sorry, I don't have the answer to that question. Would you like to contact our support team?"
                  className="min-h-[100px]"
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save & Continue</Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="preview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Preview Your Chatbot</CardTitle>
              <CardDescription>See how your chatbot will appear to users</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center justify-center lg:flex-row lg:items-start lg:gap-8">
                <div className="w-full max-w-md">
                  <ChatbotPreview />
                </div>
                <div className="mt-8 w-full max-w-md space-y-4 lg:mt-0">
                  <div className="rounded-lg border p-4">
                    <h3 className="font-medium">Installation</h3>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Add this code snippet to your website to embed the chatbot:
                    </p>
                    <pre className="mt-2 overflow-x-auto rounded-md bg-muted p-4 text-xs">
                      {`<script src="https://chatbotsaas.com/embed.js?id=YOUR_CHATBOT_ID"></script>`}
                    </pre>
                    <Button variant="outline" size="sm" className="mt-2">
                      Copy Code
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Back to Edit</Button>
              <Button>Deploy Chatbot</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

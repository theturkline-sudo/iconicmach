export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const formData = await request.json();
    
    // Example: Validate input
    if (!formData.name || !formData.email || !formData.message) {
      return new Response(JSON.stringify({ error: 'Missing required fields' }), { 
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // TODO: In a real environment, you would send an email here using an API like SendGrid, Resend, or Mailgun
    // Example: await sendEmail(formData);

    // Return success response
    return new Response(JSON.stringify({ success: true, message: 'Inquiry received' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: 'Invalid request' }), { 
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

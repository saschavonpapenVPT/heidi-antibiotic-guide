# Ready to go live?

When you are ready to go live with your Heidi integration, you can follow these steps to ensure your widget is ready for production use.

Once you received a Heidi production key:

1. Request a production API key from our Partnership Team. You would need one key for each region you are deploying to
2. Update the Authentication endpoint to `https://<region>.api.heidihealth.com/api/v2/ml-scribe/open-api/jwt`
3. Update the widget URL to: `https://widget.heidihealth.com/widget/heidi.js`
4. Update the widget configuration to include a deployment region

Heidi is currently available in these following regions:

- AU - Australia and New Zealand
- US - America
- CA - Canada
- EU - European Union
- UK - United Kingdom

If you're not sure which region certain countries are linked to, please see the region overview here

## Example production implementation

```javascript
<script>
  const heidiOptions = {
    //...
    region: 'US',
    //...
    onInit: () => {
      // ...
    },
    onReady: () => {
      // ...
    },
  };
 
  (function (s, o) {
    const script = document.createElement('script');
    script.async = true;
    script.src = s;
    document.head.append(script);
    script.addEventListener('load', () => new Heidi(o));
  })('https://widget.heidihealth.com/widget/heidi.js', heidiOptions);
</script>
```
<clientConfig version="1.1">
  <emailProvider id="centurylink.net">
    <domain>centurylink.net</domain>
    <domain>embarqmail.com</domain>
    <displayName>CenturyLink.net</displayName>
    <displayShortName>CenturyLink</displayShortName>
    <incomingServer type="pop3">
      <hostname>pop.centurylink.net</hostname>
      <port>995</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
      <pop3>
        <leaveMessagesOnServer>true</leaveMessagesOnServer>
        <!-- CenturyLink recommended setting. (see documentation link)-->
      </pop3>
    </incomingServer>
    <incomingServer type="imap">
      <hostname>mail.centurylink.net</hostname>
      <port>993</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </incomingServer>
    <!-- CenturyLink don't support IMAP. CenturyLink are providing the IMAP settings for self-help only. 
		       (see documentation links below) -->
    <outgoingServer type="smtp">
      <hostname>smtp.centurylink.net</hostname>
      <port>587</port>
      <socketType>STARTTLS</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </outgoingServer>
    <!--
        SERVER LIMITS
            Email size limit:           20MB
            Send To limit:              100 contacts
            Webmail send limit:         100 per hour
            SMTP send limit:            500 per hour
            IP-based email send limit:  50 per 5 minutes

			"Email Size Limit" refers to the size of a single email, and "Sent To Limits" 
			 include the To, CC and Bcc fields in emails. These limits are the same whether 
			 you're using webmail or SMTP.
      -->
    <documentation url="http://www.centurylink.com/help/index.php?assetid=239">
      <descr lang="en">CenturyLink | How to set up your email to go through POP3 and SMTP</descr>
    </documentation>
    <documentation url="http://www.centurylink.com/help/index.php?assetid=239#centurylinknet">
      <descr lang="en">CenturyLink | How to set up your email to go through POP3 and SMTP #Centurylink.net</descr>
    </documentation>
    <documentation url="http://www.centurylink.com/help/index.php?assetid=239#embarqmail">
      <descr lang="en">CenturyLink | How to set up your email to go through POP3 and SMTP #Embarqmail.com</descr>
    </documentation>
  </emailProvider>
</clientConfig>

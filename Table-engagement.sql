SELECT  EngagementID,
		ContentID,
		CampaignID,
		ProductID,
		UPPER(REPLACE(ContentType,'SOCIALMEDIA','SOCIAL MEDIA')) AS ContentType,
		LEFT(ViewsClicksCombined,CHARINDEX('-',ViewsClicksCombined) - 1) AS Views,
		RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-',ViewsClicksCombined)) AS Clicks,
		Likes,
		FORMAT(CONVERT(Date,EngagementDate),'dd/mm/yyyy') AS EngagementDate

FROM engagement_data

